import streamlit as st
import json
import os

# 1. 独立的数据加载函数
def load_rank_data():
    file_path = "pages/pages/hardware_rank.json"  # 确保路径与你的实际路径一致
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 2. 渲染函数（按型号独立展示评分）
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
                
                # 使用 expander 展示大类 (默认展开以便查看效果)
                with st.expander(f"**{series}**", expanded=True):
                    st.markdown(f"📝 **系列特点：** {info.get('desc', '')}")
                    st.divider()
                    
                    st.markdown("**🔍 型号细分及独立评分：**")
                    
                    # 遍历子型号，使用两列布局（左边型号和描述，右边评分）
                    for model, detail in info.get("sub_models", {}).items():
                        col_info, col_score = st.columns([1.5, 1])
                        
                        with col_info:
                            st.markdown(f"🔹 **{model}**")
                            # 使用 caption 让描述字体变小置灰，凸显层次感
                            st.caption(f"{detail.get('desc', '')}") 
                            
                        with col_score:
                            # 将该型号的评分横向排列，节省空间
                            scores = detail.get('scores', {})
                            score_text = " | ".join([f"{k}: {'⭐' * v}" for k, v in scores.items()])
                            st.markdown(f"<div style='margin-top: 10px;'>{score_text}</div>", unsafe_allow_html=True)
                            
                        # 在每个型号之间加一点间距
                        st.write("")

# 运行渲染
if __name__ == "__main__":
    render_hardware_wiki()
