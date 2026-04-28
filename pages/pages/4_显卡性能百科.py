import streamlit as st
import pandas as pd

def render_gpu_wiki():
    st.set_page_config(page_title="2026 显卡性能百科", layout="wide")
    
    # 标题区
    st.title("🎮 2026 笔记本显卡 (GPU) 性能百科")
    st.info("💡 2026年核心趋势：独显全面迈入 GDDR7 时代；RTX 50系列成为主流，老款 RTX 30/40 系作为入门高性价比选择持续存在。")

    # --- 第一部分：规格对比表 ---
    st.subheader("💻 核心显卡规格对比 (含新增型号)")
    gpu_data = {
        "显卡分类": ["旗舰/生产力", "高性能独显", "入门/上一代独显", "入门/经典独显", "高能核显", "进阶核显"],
        "显卡型号": ["NVIDIA RTX 5070 Ti", "NVIDIA RTX 5060", "NVIDIA RTX 4050", "NVIDIA RTX 3050", "Intel Arc 140V", "Radeon 780M"],
        "显存规格": ["12GB GDDR7", "8GB GDDR7", "6GB GDDR6", "4GB GDDR6", "16GB (共享)", "动态共享"],
        "显存位宽": ["192-bit", "128-bit", "96-bit", "128-bit", "128-bit", "128-bit"],
        "预期带宽": ["~512 GB/s", "~320 GB/s", "~192 GB/s", "~170 GB/s", "~136 GB/s", "~100 GB/s"],
        "性能定位": ["4K视频剪辑、骨灰级游戏", "2K高画质、AI绘图", "1080P电竞、入门创作", "基础网游、预算首选", "1080P高画质办公", "高能效比、办公全能"]
    }
    df = pd.DataFrame(gpu_data)
    st.table(df)

    # --- 新增：显卡渲染科普 ---
    with st.expander("🔍 什么时候才真正需要“显卡渲染”？ (点击展开科普)"):
        st.markdown("""
        只有当你触碰以下操作时，显卡（特别是独立显卡）才会介入并进行高强度的**“渲染”**计算：
        1. **加特效**：模糊、发光、扭曲、粒子效果。
        2. **调色**：尤其是达芬奇调色（DaVinci Resolve），极度依赖显卡算力。
        3. **转场**：复杂的 3D 效果转场。
        4. **AI 功能**：智能抠像、语音转文字（部分依赖 NPU 或 GPU 加速）。
        5. **导出**：虽然 CPU 也能导出，但显卡开启硬件加速（CUDA/NVENC）后，导出速度会快几倍。
        """)

    st.divider()

    # --- 第二部分：场景化选购建议 ---
    st.subheader("🛍️ 场景化选购建议")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("#### 1. 🚀 顶级创作与发烧游戏")
            st.markdown("**推荐型号：** :red[RTX 5070 Ti (12GB)]")
            st.markdown("**核心理由：** 12GB 大显存是处理复杂 3D 渲染和 4K 视频工作流的基石，性能远超 5060。")
            st.caption("📍 推荐机型：机械革命 苍龙 16 Ultra")

        with st.container(border=True):
            st.markdown("#### 2. 🎨 传媒艺术/视觉设计")
            st.markdown("**关注重点：** :blue[RTX 5060 + 32G 内存]")
            st.markdown("**核心理由：** 传媒专业需要稳定的 CUDA 加速。5060 具备极佳的性价比平衡点。")
            st.caption("📍 推荐机型：YOGA Pro 16、拯救者 Y7000P")

    with col2:
        with st.container(border=True):
            st.markdown("#### 3. 💰 极高性价比/学生入门")
            st.markdown("**推荐型号：** :orange[RTX 4050 / 3050]")
            st.markdown("**核心理由：** 虽然是旧架构，但在 5000-6000 元预算段依然是核显无法企及的存在。")
            st.caption("📍 推荐机型：机械革命 蛟龙 15K 系列")

        with st.container(border=True):
            st.markdown("#### 4. 🏃 超轻薄高能办公")
            st.markdown("**推荐型号：** :green[Arc 140V / Radeon 780M]")
            st.markdown("**核心理由：** 告别板砖适配器，140V 的编解码能力足以胜任日常轻度视频剪辑。")
            st.caption("📍 推荐机型：YOGA Air 14 Aura、无界 14X")

    # --- 第三部分：避坑指南 ---
    st.divider()
    st.subheader("⚠️ 显卡选购冷知识")
    
    warn_c1, warn_c2 = st.columns(2)
    
    with warn_c1:
        st.warning("""
        **【显存容量警示】** 2026年开始，**4GB 显存 (RTX 3050)** 在2K分辨率下，运行大型 3A 游戏时会出现纹理模糊或掉帧现象。如果你有专业剪辑需求，建议至少选择 **6GB (4050)** 或 **8GB (5060)** 以上型号。
        """)
        
    with warn_c2:
        st.error("""
        **【功耗释放】** 机械革命等机型通常能提供更激进的功耗释放（满血版），性能更强。而轻薄本上的显卡通常会锁功耗。  
        *提示：同型号显卡，满血版比残血版性能可高出 15%-20%。*
        """)

# 执行渲染
if __name__ == "__main__":
    render_gpu_wiki()
