import streamlit as st

# --- 配置区：以后价格变了改这里就行 ---
# 政策参数
DISCOUNT_RATE = 0.15  # 85折即补贴15%
MAX_SUBSIDY = 1500.0  # 补贴上限

# 机型数据库 (型号: [参考价格, 是否支持国补])
MODEL_DB = {
    "拯救者 Y7000P 2025 (Ultra 7 255HX)": [10999.00, True],
    "拯救者 Y9000P 2025 (Ultra 7)": [12999.00, True],
    "拯救者 R9000P 2025": [12999.00, True],
    "自定义/其他机型": [0.0, True]
}

# --- 界面展示 ---
st.set_page_config(page_title="国补计算器Pro", page_icon="🧧")
st.title("🧧 国补+店补计算器 (85折新政版)")

# 1. 机型选择
selected_model = st.selectbox("第一步：选择或搜索机型", list(MODEL_DB.keys()))
default_price, default_status = MODEL_DB[selected_model]

# 2. 参数输入
col1, col2 = st.columns(2)
with col1:
    if selected_model == "自定义/其他机型":
        price = st.number_input("商品原价 (元)", value=0.0, step=100.0)
    else:
        price = st.number_input("商品原价 (元)", value=default_price, step=1.0)

with col2:
    # 如果数据库里标记了不支持，这里会自动切换
    is_eligible = st.toggle("是否支持国补", value=default_status)

has_store_discount = st.toggle("是否有店补？")
store_discount = 0.0
if has_store_discount:
    store_discount = st.number_input("店补金额 (元)", value=0.0, step=50.0)

# --- 计算核心逻辑 ---
# 1. 先扣除店补，剩下的部分作为国补计算基数
price_after_store = price - store_discount

if is_eligible:
    # 2. 计算国补：基数 * 15%，且不超过 1500
    calc_subsidy = round(price_after_store * DISCOUNT_RATE, 2)
    gov_subsidy = min(calc_subsidy, MAX_SUBSIDY)
else:
    gov_subsidy = 0.0

final_price = price_after_store - gov_subsidy
total_saved = gov_subsidy + store_discount

# --- 结果展示 ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("最终到手价", f"¥{final_price:,.2f}")
c2.metric("国家补贴", f"¥{gov_subsidy:,.2f}")
c3.metric("总计优惠", f"¥{total_saved:,.2f}")

# 补充提示
if gov_subsidy >= MAX_SUBSIDY:
    st.warning(f"💡 该机型已达到国补上限 ¥{MAX_SUBSIDY}")
elif is_eligible:
    st.info(f"💡 当前按 85 折计算 (补贴比例 {DISCOUNT_RATE*100}%)")

if st.button("生成详细清单", use_container_width=True):
    st.code(f"""
    【订单明细表】
    --------------------------
    所选机型：{selected_model}
    商品原价：¥{price:,.2f}
    店铺优惠：-¥{store_discount:,.2f}
    国家补贴：-¥{gov_subsidy:,.2f} ({'15%补贴' if is_eligible else '不支持'})
    --------------------------
    实付金额：¥{final_price:,.2f}
    """, language="text")
