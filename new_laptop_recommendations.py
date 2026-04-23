import streamlit as st
import pandas as pd
import json

def calculate_subsidy(price):
    return price - min(price * 0.15, 1500)

def get_pro_advice(cpu, ram, gpu):
    """根据配置从 JSON 库提取建议"""
    advices = []
    # 匹配 CPU 建议
    for key, text in ADVICE_DATA["CPU"].items():
        if key.lower() in cpu.lower():
            advices.append(f"🔍 **处理器**: {text}")
            break
    # 匹配 内存 建议
    for key, text in ADVICE_DATA["RAM"].items():
        if key.lower() in ram.lower():
            advices.append(f"🧠 **存储**: {text}")
            break
    # 匹配 显卡 建议
    for key, text in ADVICE_DATA["GPU"].items():
        if key.lower() in gpu.lower():
            advices.append(f"🎮 **图形**: {text}")
            break
    return advices

# --- 3. Streamlit UI ---
st.set_page_config(page_title="2026 大学生选购专家", layout="wide")
st.title("🎓 智能电脑选购：配置比对与避雷建议")

with st.sidebar:
    st.header("🔍 核心需求")
    major = st.selectbox("学科类别", ["理工/仿真", "计算机/编程", "传媒/设计", "文管/办公"])
    budget = st.slider("预算 (国补后)", 4000, 15000, 8000)
    portability = st.toggle("需要轻便 (背着不累)")

# 过滤逻辑
results = []
for brand, models in MODEL_DB.items():
    for name, data in models.items():
        f_price = calculate_subsidy(data["price"])
        if f_price <= budget:
            # 简单轻便过滤
            if portability and any(x in name for x in ["拯救者", "暗影精灵"]):
                continue
            
            results.append({
                "brand": brand,
                "name": name,
                "price": f_price,
                "specs": data["specs"]
            })

# --- 4. 结果展示与建议分析 ---
if results:
    st.subheader(f"✨ 为你精选了 {len(results)} 款机型")
    
    for item in results:
        cpu, ram, ssd, gpu, screen, refresh = item["specs"]
        
        # 使用 Streamlit 的容器美化每款机型的展示
        with st.expander(f"📌 {item['brand']} {item['name']} | 国补后: ¥{item['price']:.2f}"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write("**硬件参数**")
                st.write(f"- CPU: `{cpu}`")
                st.write(f"- 内存: `{ram}`")
                st.write(f"- 显卡: `{gpu}`")
                st.write(f"- 屏幕: `{screen} / {refresh}`")
            
            with col2:
                st.write("**💡 专家建议 (基于配置库提取)**")
                # 提取并显示建议
                advices = get_pro_advice(cpu, ram, gpu)
                if advices:
                    for a in advices:
                        st.info(a)
                else:
                    st.write("该配置暂无针对性建议，请查看官方评测。")
else:
    st.error("没有找到符合要求的机型，请尝试提高预算或取消‘轻便’要求。")

st.markdown("---")
st.caption("提示：建议库由 AI 与 2026 市场调研总结，数据仅供参考。")
