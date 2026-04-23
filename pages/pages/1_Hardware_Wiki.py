import streamlit as st
import json
import os

# 1. 独立的数据加载函数
def load_rank_data():
    file_path = "pages/pages/hardware_rank.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 2. 渲染函数（针对多层 JSON 优化版）
def render_hardware_wiki():
    st.set_page_config(page_title="CPU 性能天梯 - 2026", layout="wide")
    st.title("📊 2026 笔记本 CPU 性能百科")
    
    rank_db = load_rank_data()
    if not rank_db:
        st.error("未找到 hardware_rank.json 数据库！")
        return

    brand_tabs = st.tabs(["Intel 阵营", "AMD 阵营"])
    
    # 遍历品牌 (Intel/AMD)
    for i, brand in enumerate(["Intel", "AMD"]):
        with brand_tabs[i]:
            categories = rank_db.get(brand, {})
            for series, info in categories.items():
                # 使用 expander 展示大类
                with st.expander(f"**{series}**", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"📝 **系列特点：**\n{info['desc']}")
                        st.divider()
                        st.markdown("**🔍 型号细分及定位：**")
                        # 遍历子型号
                        for model, detail in info.get("sub_models", {}).items():
                            st.write(f"🔹 **{model}**：{detail}")
                    
                    with col2:
                        st.markdown("**⭐ 性能评级**")
                        for metric, score in info['scores'].items():
                            st.write(f"{metric}: {'⭐' * score}")

# 运行渲染
if __name__ == "__main__":
    render_hardware_wiki()
