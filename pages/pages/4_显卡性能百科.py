import streamlit as st
import pandas as pd

def render_gpu_wiki():
    st.set_page_config(page_title="2026 显卡性能百科", layout="wide")
    
    # 标题区
    st.title("🎮 2026 笔记本显卡 (GPU) 性能百科")
    st.info("💡 2026年核心趋势：独显全面迈入 GDDR7 时代，核显带宽突破 130GB/s。")

    # --- 第一部分：规格对比表 ---
    st.subheader("💻 核心显卡规格对比")
    gpu_data = {
        "显卡分类": ["高性能独显", "高能核显", "进阶核显", "入门核显"],
        "显卡型号": ["NVIDIA RTX 5060", "Intel Arc 140V", "Radeon 780M", "Intel Arc (Ultra 5)"],
        "显存容量": ["8GB GDDR7", "16GB (共享)", "动态共享", "动态共享"],
        "显存位宽": ["128-bit", "128-bit (LPDDR5x)", "128-bit (DDR5/LP5)", "128-bit"],
        "预期带宽": ["~320 GB/s", "~136 GB/s", "~100 GB/s", "~80 GB/s"],
        "性能定位": ["2K高画质、3D渲染、AI绘图", "1080P网游、视频剪辑", "高能效比、办公全能", "基础办公、高清视频"]
    }
    df = pd.DataFrame(gpu_data)
    # 使用 dataframe 展示，并设置高度适配内容
    st.table(df)

    st.divider()

    # --- 第二部分：场景化选购建议 ---
    st.subheader("🛍️ 场景化选购建议")
    
    # 使用两行两列的布局
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("#### 1. 🎮 游戏玩家与 AI 创作")
            st.markdown("**推荐型号：** :orange[RTX 5060]")
            st.markdown("**核心理由：** GDDR7 显存带来的带宽飞跃，是流畅运行 3A 大作和本地部署 AI 模型 (Stable Diffusion) 的入场券。")
            st.caption("📍 推荐机型：拯救者 Y7000P、暗影精灵 10")

        with st.container(border=True):
            st.markdown("#### 2. 🎨 传媒艺术/视觉设计")
            st.markdown("**关注重点：** :blue[内存 32G + 2K 高分屏]")
            st.markdown("**核心理由：** 剪辑更吃内存。核显如 Arc 140V 在 4K 解码有优势，但必须匹配高色准 OLED 屏。")
            st.caption("📍 推荐机型：YOGA Pro 16、小新 Pro 16 GT")

    with col2:
        with st.container(border=True):
            st.markdown("#### 3. 🏃 便携办公与高效能")
            st.markdown("**推荐型号：** :green[Arc 140V / Radeon 780M]")
            st.markdown("**核心理由：** 兼顾离电续航与轻度娱乐（原神/英雄联盟），无需背负厚重电源。")
            st.caption("📍 推荐机型：YOGA Air 14、小新 Pro 14c")

        with st.container(border=True):
            st.markdown("#### 4. 📺 日常影音与家用")
            st.markdown("**推荐型号：** :gray[Intel/UHD Graphics]")
            st.markdown("**核心理由：** 带宽不是瓶颈，足以胜任 Office 套件和多网页浏览。")
            st.caption("📍 推荐机型：星Book 15、入门款小新")

    # --- 第三部分：避坑指南 ---
    st.divider()
    st.subheader("⚠️ 选购避坑指南")
    
    warn_c1, warn_c2 = st.columns(2)
    
    with warn_c1:
        st.warning("""
        **【内存陷阱】** 核显性能极其依赖物理内存。如果你选核显机型，**强烈建议直上 32GB 内存**。  
        *原因：核显会强制划走一部分内存作为显存。*
        """)
        
    with warn_c2:
        st.error("""
        **【带宽瓶颈】** 对于传媒工作，**屏幕分辨率需求普遍高于 2K **。  
        *提示：请剔除所有 1080P 分辨率的候选机型，它会严重限制你的预览视野。*
        """)

# 执行渲染
if __name__ == "__main__":
    render_gpu_wiki()
