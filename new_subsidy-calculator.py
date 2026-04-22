import streamlit as st

# --- 配置区 ---
DISCOUNT_RATE = 0.15  # 85折
MAX_SUBSIDY = 1500.0  # 补贴上限

# 升级后的数据库：[价格, 是否国补, CPU, 内存, 硬盘, 显卡, 分辨率, 刷新率]
MODEL_DB = {
    "联想 拯救者 Y7000P 2025 (Ultra 7 255HX)": {
        "price": 10999.0, "status": True,
        "specs": ["Ultra 7 255HX", "16G", "1T", "RTX 5060", "2.5K", "165Hz"]
    },
    "联想 拯救者 Y9000P 2025 (Ultra 9)": {
        "price": 12999.0, "status": True,
        "specs": ["Ultra 9 285HX", "32G", "1T", "RTX 5060", "2.5K", "240Hz"]
    },
    "联想 拯救者 R9000P 2025": {
        "price": 12999.0, "status": True,
        "specs": ["Ryzen 9 8945HX", "32G", "1T", "RTX 5060", "2.5K", "240Hz"]
    },
    "自定义/其他机型": {
        "price": 0.0, "status": True,
        "specs": ["-", "-", "-", "-", "-", "-"]
    }
}

st.set_page_config(page_title="国补计算器Pro", page_icon="🧧", layout="wide")
st.title("🧧 国补+店补价格计算器")

# 1. 选择机型
selected_model = st.selectbox("第一步：选择或搜索机型", list(MODEL_DB.keys()))
model_data = MODEL_DB[selected_model]

# --- 新增：参数展示区 ---
if selected_model != "自定义/其他机型":
    with st.expander("🔍 查看机型详细配置", expanded=True):
        s = model_data["specs"]
        cols = st.columns(6)
        labels = ["CPU型号", "内存大小", "硬盘大小", "显卡型号", "分辨率", "刷新率"]
        for i in range(6):
            cols[i].caption(labels[i])
            cols[i].write(f"**{s[i]}**")

st.divider()

# 2. 参数输入
col_a, col_b = st.columns(2)
with col_a:
    price = st.number_input("商品原价 (元)", value=model_data["price"], step=1.0)
with col_b:
    is_eligible = st.toggle("是否支持国补", value=model_data["status"])

has_store_discount = st.toggle("是否有店补？")
store_discount = 0.0
if has_store_discount:
    store_discount = st.number_input("店补金额 (元)", value=0.0, step=50.0)

# --- 计算逻辑 ---
price_after_store = price - store_discount
gov_subsidy = min(round(price_after_store * DISCOUNT_RATE, 2), MAX_SUBSIDY) if is_eligible else 0.0
final_price = price_after_store - gov_subsidy
total_saved = gov_subsidy + store_discount

# --- 结果展示 ---
c1, c2, c3 = st.columns(3)
c1.metric("最终到手价", f"¥{final_price:,.2f}")
c2.metric("国家补贴", f"¥{gov_subsidy:,.2f}")
c3.metric("总计优惠", f"¥{total_saved:,.2f}")

if gov_subsidy >= MAX_SUBSIDY:
    st.warning(f"💡 该机型已达到国补上限 ¥{MAX_SUBSIDY}")

if st.button("生成详细清单", use_container_width=True):
    specs_text = " / ".join(model_data["specs"]) if selected_model != "自定义/其他机型" else "自定义配置"
    st.code(f"""
    【订单明细表】
    --------------------------
    机型配置：{selected_model}
    核心规格：{specs_text}
    --------------------------
    商品原价：¥{price:,.2f}
    店铺优惠：-¥{store_discount:,.2f}
    国家补贴：-¥{gov_subsidy:,.2f} (15%)
    --------------------------
    实付金额：¥{final_price:,.2f}
    """, language="text")
