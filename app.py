import streamlit as st

# 设置页面配置（手机端适配更好）
st.set_page_config(page_title="国补计算器", layout="centered")

st.title("🧧 国补+店补价格计算器")
st.write("输入参数，实时计算最终到手价")

# --- 输入部分 ---
with st.container():
    price = st.number_input("商品原价（元）", min_value=0.0, step=100.0, value=5000.0)
    
    has_shop_discount = st.toggle("是否有店补？", value=False)
    
    shop_discount = 0.0
    if has_shop_discount:
        shop_discount = st.number_input("店补减免金额（元）", min_value=0.0, step=10.0)

# --- 计算逻辑 ---
intermediate_price = max(0.0, price - shop_discount)

if intermediate_price <= 10000:
    national_subsidy = intermediate_price * 0.15
    final_price = intermediate_price * 0.85
else:
    national_subsidy = 1500
    final_price = intermediate_price - 1500

total_discount = shop_discount + national_subsidy

# --- 展示部分 ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.metric("最终到手价", f"¥{final_price:.2f}")
with col2:
    st.metric("总优惠", f"¥{total_discount:.2f}", delta=f"含国补{national_subsidy:.2f}")

if st.button("生成详细清单", use_container_width=True):
    st.info(f"""
    - **原始价格**: ¥{price:.2f}
    - **店补金额**: -¥{shop_discount:.2f}
    - **国补金额**: -¥{national_subsidy:.2f} (基于 {intermediate_price:.2f} 计算)
    """)
