import streamlit as st
import pandas as pd
import json
import os

# --- 1. 数据加载模块 ---
def load_data():
    if os.path.exists("laptops.json"):
        with open("laptops.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_tips():
    if os.path.exists("tips.json"):
        with open("tips.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

MODEL_DB = load_data()
TIPS_DB = load_tips()

# --- 2. 逻辑计算模块 ---
def calculate_subsidy(price):
    """2026年国补标准：15%补贴，最高1500元"""
    return price - min(price * 0.15, 1500)

# --- 3. Streamlit UI ---
st.set_page_config(page_title="大学生选购助手 2026", layout="wide")
st.title("🎓 大学生电脑选购智能推荐 (2026 国补版)")

with st.sidebar:
    st.header("🔍 你的需求")
    major_type = st.selectbox("选择你的学科类别", 
        ["理工科 (仿真/建模/渲染)", "计算机/软件 (编程/虚拟机)", "传媒/艺术 (剪辑/设计)", "文管/通用 (办公/刷课)"])
    
    budget = st.slider("你的预算上限 (国补后价格)", 3000, 14000, 8000)
    gaming_need = st.checkbox("有重度游戏需求 (3A大作)")
    portability_first = st.checkbox("优先考虑便携性 (常带去图书馆)")

# --- 4. 核心功能：基于建议库的智能贴士 ---
if TIPS_DB:
    with st.expander("✨ 针对你专业的选购小贴士", expanded=True):
        # 自动匹配当前学科的建议
        scenario_tip = TIPS_DB["scenarios"].get(major_type, "选择专业以查看定制建议")
        st.info(scenario_tip)
        
        # 动态解析 CPU 类型
        st.caption("🔍 **快速避坑：** " + " | ".join([f"**{k}**: {v}" for k, v in TIPS_DB["cpu_wiki"].items()]))

# --- 5. 过滤与推荐算法 ---
st.subheader("💡 为你匹配的机型")

recommendations = []
for brand, models in MODEL_DB.items():
    if brand == "自定义": continue
    
    for name, data in models.items():
        # 排除非笔记本项
        if any(kw in name for kw in ["一体机", "AIO", "台式"]): continue
        
        price = data["price"]
        cpu, ram, ssd, gpu, screen, refresh = data["specs"]
        final_price = calculate_subsidy(price)
        
        # 性能标签化
        is_gaming_perf = "5060" in gpu or "5070" in gpu
        is_high_cpu = any(x in cpu for x in ["Ultra 7", "Ultra 9", "Ryzen 9", "i9"])
        
        # 匹配逻辑
        is_match = True
        if final_price > budget: is_match = False
        
        # 匹配专业需求
        if (gaming_need or "理工" in major_type) and not is_gaming_perf:
            is_match = False
        elif ("传媒" in major_type or "计算机" in major_type) and not (is_gaming_perf or is_high_cpu):
            is_match = False
            
        # 便携性过滤（排除厚重游戏品牌）
        if portability_first and any(kw in name for kw in ["拯救者", "暗影精灵", "极光"]):
            is_match = False

        if is_match:
            recommendations.append({
                "品牌": brand,
                "型号": name,
                "原价": price,
                "国补后": final_price,
                "核心配置": f"{cpu} | {ram} | {gpu}",
                "屏幕": f"{screen} / {refresh}"
            })

# --- 6. 结果展示 ---
if recommendations:
    df = pd.DataFrame(recommendations).sort_values(by="国补后", ascending=True)
    
    # 格式化输出
    df_display = df.copy()
    df_display["原价"] = df_display["原价"].apply(lambda x: f"¥{x:.0f}")
    df_display["国补后"] = df_display["国补后"].apply(lambda x: f"¥{x:.2f}")
    
    st.table(df_display.reset_index(drop=True))
    
    # 额外反馈
    best_deal = df.iloc[0]
    st.success(f"✅ 最省钱方案：**{best_deal['型号']}**，国补后仅需 **¥{best_deal['国补后']:.2f}**")
else:
    st.warning("☹️ 当前预算下未找到完美匹配，建议稍微调高预算或放宽便携性要求。")

st.info("💡 提示：以上数据实时调用 2026 建议库。")

# 侧边栏导航
page = st.sidebar.radio("功能切换", ["智能机型推荐", "硬件性能百科"])

if page == "智能机型推荐":
    # 执行推荐逻辑
    run_recommendation_ui() # 建议把推荐逻辑封装成函数
else:
    # 执行百科逻辑
    render_hardware_wiki(RANK_DB)
