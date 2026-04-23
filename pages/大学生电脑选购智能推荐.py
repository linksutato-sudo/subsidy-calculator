import streamlit as st
import pandas as pd
import json
import os

# --- 1. 数据加载模块 ---
def load_data():
    # 模拟数据，实际使用时请确保 laptops.json 存在
    if os.path.exists("laptops.json"):
        with open("laptops.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "惠普 (HP)": {
            "暗影精灵 10 (i7-14650HX)": {"price": 8999, "specs": ["i7-14650HX", "16G", "1TB", "RTX 5060", "2.5K", "240Hz"]},
            "光影精灵 11 悦龙版": {"price": 9299, "specs": ["Ryzen 7 255", "24GB", "1TB", "RTX 5060 8G", "1080P FHD", "144Hz"]}
        }
    }

def load_tips():
    if os.path.exists("tips.json"):
        with open("tips.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "scenarios": {
            "理工科 (仿真/建模/渲染)": "理工科建议：你的专业软件非常吃单核频率和显卡算力，认准 CPU 后缀为 'HX' 的机型。",
            "计算机/软件 (编程/虚拟机)": "码农建议：内存 32G 起步，否则虚拟机和 IDE 会让你痛不欲生。",
            "传媒/艺术 (剪辑/设计)": "设计建议：屏幕色准（DCI-P3）是第一优先级，显卡次之。",
            "文管/通用 (办公/刷课)": "通用建议：优先选 Ultra 系列，续航能打一整天，风扇安静。"
        }
    }

MODEL_DB = load_data()
TIPS_DB = load_tips()

# --- 2. 逻辑计算模块 ---
def calculate_subsidy(price):
    """2026年国补标准：15%补贴，最高1500元"""
    return price - min(price * 0.15, 1500)

# --- 3. 页面配置 ---
st.set_page_config(page_title="大学生选购助手 2026", layout="wide", page_icon="🎓")

# 自定义 CSS 样式（美化底部百科）
st.markdown("""
    <style>
    .baike-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f2f6;
        border: 1px solid #e0e4eb;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 侧边栏：核心过滤需求 ---
with st.sidebar:
    st.title("🔍 需求定义")
    major_type = st.selectbox("选择你的学科类别", 
        ["理工科 (仿真/建模/渲染)", "计算机/软件 (编程/虚拟机)", "传媒/艺术 (剪辑/设计)", "文管/通用 (办公/刷课)"])
    
    budget = st.slider("你的预算上限 (国补后)", 3000, 14000, 8000)
    
    st.write("---")
    gaming_need = st.checkbox("有重度游戏需求 (3A大作)")
    portability_first = st.checkbox("优先考虑便携性")
    
    st.info("💡 侧边栏调整参数，右侧结果实时更新")

# --- 5. 主体内容：贴士与结果 ---
st.title("🎓 大学生电脑选购智能推荐 (2026 国补版)")

# 5.1 专业贴士
with st.container():
    if TIPS_DB:
        scenario_tip = TIPS_DB["scenarios"].get(major_type, "选择专业以查看定制建议")
        st.warning(f"✨ **针对{major_type[:3]}的选购建议**：{scenario_tip}")

# 5.2 推荐列表
st.subheader("💡 为你匹配的机型")

recommendations = []
for brand, models in MODEL_DB.items():
    if brand == "自定义": continue
    for name, data in models.items():
        price = data["price"]
        cpu, ram, ssd, gpu, screen, refresh = data["specs"]
        final_price = calculate_subsidy(price)
        
        # 简化版逻辑判定 (沿用你之前的逻辑)
        ram_val = int(''.join(filter(str.isdigit, ram))) 
        is_2k_plus = any(x in screen.upper() for x in ["2K", "2.5K", "2.8K", "3K", "4K"])
        is_gaming_perf = "5060" in gpu or "5070" in gpu
        
        is_match = True
        if final_price > budget: is_match = False
        if (gaming_need or "理工" in major_type) and not is_gaming_perf: is_match = False
        if portability_first and any(kw in name for kw in ["暗影精灵", "拯救者"]): is_match = False

        if is_match:
            recommendations.append({
                "品牌": brand, "型号": name, "原价": price, "国补后": final_price,
                "核心配置": f"{cpu} | {ram} | {gpu}", "屏幕": f"{screen} / {refresh}"
            })

if recommendations:
    df = pd.DataFrame(recommendations).sort_values(by="国补后", ascending=True)
    df_display = df.copy()
    df_display["原价"] = df_display["原价"].apply(lambda x: f"¥{x:.0f}")
    df_display["国补后"] = df_display["国补后"].apply(lambda x: f"¥{x:.2f}")
    
    st.table(df_display.reset_index(drop=True))
    
    best_deal = df.iloc[0]
    st.success(f"✅ 最省钱方案：**{best_deal['型号']}**，国补后仅需 **¥{best_deal['国补后']:.2f}**")
else:
    st.warning("☹️ 当前预算下未找到完美匹配。")

# --- 6. 底部：百科导向 ---
st.write("---")
st.subheader("📚 硬件知识百科")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="baike-card"><b>💻 CPU 性能榜</b><br><small>HX vs Ultra 怎么选</small></div>', unsafe_allow_html=True)
    if st.button("查看 CPU 百科", key="cpu"):
        st.info("2026 趋势：HX 依然是性能王者，但 Ultra 2代在离电性能上已实现反超。")

with col2:
    st.markdown('<div class="baike-card"><b>🎮 显卡天梯图</b><br><small>RTX 50系列移动端解析</small></div>', unsafe_allow_html=True)
    if st.button("查看显卡百科", key="gpu"):
        st.info("RTX 5060 现已支持显存压缩技术，入门级建模效率提升 30%。")

with col3:
    st.markdown('<div class="baike-card"><b>🎞️ 屏幕色域科普</b><br><small>100% P3 是刚需吗</small></div>', unsafe_allow_html=True)
    if st.button("查看屏幕百科", key="screen"):
        st.info("传媒学子必看：如果你不买校色仪，请认准出厂校色 delta E < 2 的机型。")

with col4:
    st.markdown('<div class="baike-card"><b>🔋 续航与 NPU</b><br><small>AI 时代如何选轻薄本</small></div>', unsafe_allow_html=True)
    if st.button("查看 AI 百科", key="ai"):
        st.info("NPU 算力超过 40 TOPS 才是合格的 2026 AI PC。")

st.markdown("<br><br><center style='color:gray'>© 2026 大学生选购助手 | 数据实时更新于 2026-04</center>", unsafe_allow_html=True)
