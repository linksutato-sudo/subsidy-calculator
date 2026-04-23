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

st.set_page_config(page_title="国补计算器Pro", page_icon="🧧", layout="wide")
st.title("🧧 国补+店补价格计算器")

# --- 第一步：二级联动选择 ---
c1, c2 = st.columns(2)
with c1:
    selected_brand = st.selectbox("1. 选择品牌", list(MODEL_DB.keys()))

# 根据选中的品牌，动态生成机型列表
model_options = MODEL_DB[selected_brand]

with c2:
    selected_model = st.selectbox("2. 选择具体机型", list(model_options.keys()))

model_data = model_options[selected_model]

# --- 参数展示区 ---
if selected_brand != "自定义":
    with st.expander("🔍 查看机型详细配置", expanded=True):
        s = model_data["specs"]
        cols = st.columns(6)
        labels = ["CPU型号", "内存大小", "硬盘大小", "显卡型号", "分辨率", "刷新率"]
        for i in range(6):
            cols[i].caption(labels[i])
            cols[i].write(f"**{s[i]}**")

st.divider()

# --- 第二步：价格与补贴调整 ---
col_a, col_b = st.columns(2)
with col_a:
    # 使用 key 确保在切换机型时 number_input 能够刷新
    price = st.number_input("商品原价 (元)", value=model_data["price"], step=1.0, key=f"p_{selected_model}")
with col_b:
    is_eligible = st.toggle("是否支持国补", value=model_data["status"], key=f"t_{selected_model}")

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
res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric("最终到手价", f"¥{final_price:,.2f}")
res_col2.metric("国家补贴", f"¥{gov_subsidy:,.2f}")
res_col3.metric("总计优惠", f"¥{total_saved:,.2f}")

if gov_subsidy >= MAX_SUBSIDY:
    st.warning(f"💡 该机型已达到国补上限 ¥{MAX_SUBSIDY}")

if st.button("生成详细清单", use_container_width=True):
    specs_text = " / ".join(model_data["specs"]) if selected_brand != "自定义" else "自定义配置"
    st.code(f"""
    【订单明细表】
    --------------------------
    所属品牌：{selected_brand}
    机型配置：{selected_model}
    核心规格：{specs_text}
    --------------------------
    商品原价：¥{price:,.2f}
    店铺优惠：-¥{store_discount:,.2f}
    国家补贴：-¥{gov_subsidy:,.2f} (15%)
    --------------------------
    实付金额：¥{final_price:,.2f}
    """, language="text")
