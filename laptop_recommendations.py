import streamlit as st
import pandas as pd
import json  # 必须导入这个库
import os

# 定义一个读取数据的函数
def load_data():
    file_path = "laptops.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error("未找到数据库文件 laptops.json！")
        return {}

# 调用函数获取数据库
MODEL_DB = load_data()

# --- 后续的 calculate_subsidy 和 Streamlit 逻辑保持不变 ---

def calculate_subsidy(price):
    """计算2026年国补后的价格（15%补贴，最高1500）"""
    subsidy_amount = min(price * 0.15, 1500)
    return price - subsidy_amount

# --- Streamlit UI 界面 ---
st.set_page_config(page_title="大学生选购助手 2026", layout="wide")
st.title("🎓 大学生电脑选购智能推荐 (2026 国补版)")

# 侧边栏：用户需求输入
with st.sidebar:
    st.header("🔍 你的需求")
    major_type = st.selectbox("选择你的学科类别", 
        ["理工科 (仿真/建模/渲染)", "计算机/软件 (编程/虚拟机)", "传媒/艺术 (剪辑/设计)", "文管/通用 (办公/刷课)"])
    
    budget = st.slider("你的预算范围 (国补后价格)", 3000, 14000, 7000)
    gaming_need = st.checkbox("有重度游戏需求 (3A大作)")
    portability_first = st.checkbox("优先考虑便携性 (经常带去图书馆)")

# 逻辑过滤
st.subheader("💡 为你匹配的机型")

recommendations = []
for brand, models in MODEL_DB.items():
    if brand == "自定义": continue # 跳过手动输入示例逻辑
    
    for name, data in models.items():
        # 1. 提取原始数据
        price = data["price"]
        cpu, ram, ssd, gpu, screen, refresh = data["specs"]
        
        # 2. 计算补贴后价格 (关键修复：定义 final_price)
        final_price = calculate_subsidy(price)
        
        # 3. 定义性能特征
        is_gaming_perf = "5060" in gpu or "5070" in gpu
        is_design_perf = is_gaming_perf or any(x in cpu for x in ["Ultra 7", "Ultra 9", "Ryzen 7", "Ryzen 9", "i7", "i9"])
        
        # 4. 匹配逻辑
        is_match = True
        
        # 预算过滤
        if final_price > budget:
            is_match = False
        
        # 性能/专业匹配
        if gaming_need or "理工" in major_type:
            # 游戏和理工科强需求 GPU
            if not is_gaming_perf: 
                is_match = False
        elif "传媒" in major_type or "计算机" in major_type:
            # 传媒和计算机需要较强的 CPU 或全能配置
            if not is_design_perf: 
                is_match = False
        
        # 便携性过滤
        if portability_first:
            # 排除厚重的游戏本系列
            if any(keyword in name for keyword in ["拯救者", "暗影精灵", "光影精灵"]):
                is_match = False

        if is_match:
            recommendations.append({
                "品牌": brand,
                "型号": name,
                "原价": f"¥{price:.0f}",
                "国补后": f"¥{final_price:.2f}",
                "核心配置": f"{cpu} | {ram} | {gpu}",
                "屏幕": f"{screen} / {refresh}"
            })

# --- 结果显示区域 ---
if recommendations:
    df = pd.DataFrame(recommendations)
    st.dataframe(df, use_container_width=True) # 使用 dataframe 交互感更好
else:
    st.warning("暂无完全匹配机型，建议适当增加预算或放宽要求。")

st.info("💡 提示：2026年国补单件最高省1500元，以上价格仅供参考。")
