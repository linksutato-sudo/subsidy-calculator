import streamlit as st

def render_memory_wiki():
    st.set_page_config(page_title="2026 内存性能百科", layout="wide")
    st.title("🧠 2026 笔记本内存 (RAM) 选购百科")
    st.caption("数据更新至 2026 年 Q2 | 涵盖容量、频率、通道及选购逻辑")

    # --- 核心选购建议卡片 ---
    st.subheader("💡 快速选购建议")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("日常办公", "16GB", "2x8GB 双通道")
    with c2:
        st.metric("专业剪辑/游戏", "32GB", "2x16GB 双通道")
    with c3:
        st.metric("极端渲染/科研", "48GB+", "高频 DDR5")
    
    st.divider()

    # --- 详细分类展示 ---
    tab1, tab2, tab3 = st.tabs(["📏 按容量划分", "⚡ 按频率划分", "🔧 升级与兼容性"])

    with tab1:
        st.markdown("### 内存容量与适用场景")
        col_cap1, col_cap2 = st.columns(2)
        
        with col_cap1:
            with st.expander("🔹 **基础容量 (≤16GB)**", expanded=True):
                st.write("**配置：** 1x16GB 或 2x8GB")
                st.write("**场景：** 网页浏览、PPT办公、学生作业")
                st.success("✅ 优势：满足 90% 用户需求，性价比最高。")
            
            with st.expander("🔹 **中高端容量 (24-32GB)**"):
                st.write("**配置：** 2x12GB 或 2x16GB")
                st.write("**场景：** 3D建模(Blender)、4K视频剪辑、3A游戏大作")
                st.info("ℹ️ 建议：专业设计工作者的入门标准。")

        with col_cap2:
            with st.expander("🔹 **专业级容量 (≥48GB)**"):
                st.write("**配置：** 2x24GB 或 4x16GB")
                st.write("**场景：** 科学计算、深度学习、大规模虚拟机")
                st.warning("⚠️ 提示：需确认笔记本主板是否支持单条 24GB 或更高容量。")

    with tab2:
        st.markdown("### 内存频率与性能表现")
        freq_data = [
            ["DDR4", "3200MHz", "主流", "兼容性极佳，适合旧款或入门本"],
            ["DDR5", "5200/5600MHz", "主流", "2026年主流游戏本标配"],
            ["DDR5", "6400MHz", "高端", "配合 i9/Ryzen 9 提升约 15% 性能"],
            ["LPDDR5X", "7467MHz", "顶级", "仅限高端轻薄本，带宽提升显著"]
        ]
        st.table({"类型": [x[0] for x in freq_data], 
                  "频率": [x[1] for x in freq_data], 
                  "定位": [x[2] for x in freq_data], 
                  "评价": [x[3] for x in freq_data]})
        
        st.info("🔥 **性能小知识：** 双通道内存比单通道带宽提升约 **80%**，对核显性能有决定性影响。")

    with tab3:
        st.markdown("### 升级避坑指南")
        
        col_rule1, col_rule2 = st.columns(2)
        with col_rule1:
            st.markdown("""
            #### 1. 物理结构确认
            * **轻薄本：** 多为 **板载内存 (On-board)**，焊死在主板，**无法升级**。
            * **游戏本/全能本：** 通常提供 **2个插槽**，支持后期更换。
            """)
        
        with col_rule2:
            st.markdown("""
            #### 2. 兼容性原则
            * **同频原则：** 混用不同频率时，系统会自动以 **最低频率** 运行。
            * **品牌建议：** 尽量选择相同品牌/颗粒，避免内存冲突导致蓝屏。
            """)
        
        st.error("❗ **特别注意：** LPDDR5X 虽然频率高 (7467MHz)，但全部是焊死的，买前必须选好容量！")

if __name__ == "__main__":
    render_memory_wiki()
