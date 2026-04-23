import streamlit as st

# --- 配置区 ---
DISCOUNT_RATE = 0.15  # 85折
MAX_SUBSIDY = 1500.0  # 补贴上限

# 升级后的数据库：按品牌分类 [价格, 是否国补, CPU, 内存, 硬盘, 显卡, 分辨率, 刷新率]
MODEL_DB = {
    "联想 (Lenovo)": {
       "拯救者 Y7000P IRX10 (i7-14650HX/1T)": {
            "price": 11999.0, 
            "status": True,
            "specs": ["i7-14650HX", "16GB", "1TB", "RTX 5060 8G", "2.5K", "240Hz"]
        },
        "拯救者 Y7000P IRX10 (i9-14900HX)": {
            "price": 12999.0, 
            "status": True,
            "specs": ["i9-14900HX", "16GB", "1TB", "RTX 5060 8G", "2.5K", "240Hz"]
        },
        "拯救者 Y7000P IRX10 (i7-14650HX/512G)": {
            "price": 10999.0, 
            "status": True,
            "specs": ["i7-14650HX", "16GB", "512GB", "RTX 5060 8G", "2.5K", "240Hz"]
        },
        "拯救者 R7000P ADR10": {
            "price": 12999.0, 
            "status": True,
            "specs": ["Ryzen 9 8945HX", "16GB", "1TB", "RTX 5060 8G", "2.5K", "240Hz"]
        },
        "小新 一体机 27-IRH (i5-13420H)": {
            "price": 7099.0, 
            "status": True,
            "specs": ["i5-13420H", "16GB", "1TB", "Intel UHD Graphics", "1080P", "100Hz"]
        },
        "小新 Pro 16 2026 AI元启版": {
            "price": 9999.0, 
            "status": True,
            "specs": ["Ultra 5 336H", "32GB", "1TB", "Intel Graphics", "15.9寸", "2.8K", "120Hz OLED"]
        },
        "小新 14 AHP10R": {
            "price": 5999.0, 
            "status": True,
            "specs": ["Ryzen 7 H 255", "16GB", "512GB", "Radeon 780M", "1920*1200", "60Hz"]
        },
        "小新 Pro 14c AHP10R": {
            "price": 7499.0, 
            "status": True,
            "specs": ["Ryzen 7 H 255", "32GB", "1TB", "Radeon 780M", "2.8K", "120Hz OLED"]
        },
        "小新 Pro 16c AHP10R": {
            "price": 7999.0, 
            "status": True,
            "specs": ["Ryzen 7 H 255", "32GB", "1TB", "Radeon 780M", "2.8K", "120Hz OLED"]
        },
        "小新 16c AHP10": {
            "price": 6499.0, 
            "status": True,
            "specs": ["Ryzen 7 8745HS", "16GB", "512GB", "Radeon 780M", "1920*1200", "60hZ"]
        },
        "小新 Pro 16 GT AI元启版": {
            "price": 7999.0, 
            "status": True,
            "specs": ["Ultra 5 225H", "32GB", "1TB", "Intel Arc 130T", "2.8K", "120Hz OLED"]
        },
        "YOGA Pro 16 IAH10": {
            "price": 11999.0, 
            "status": True,
            "specs": ["Ultra 9 285H", "32GB", "1TB", "RTX 5060 8G", "2.8K", "120Hz OLED"]
        },
        "YOGA Air 14 Aura AI元启版": {
            "price": 9999.0, 
            "status": True,
            "specs": ["Ultra 7 258V", "32GB", "1TB", "Intel Arc 140V", "2.8K", "120Hz OLED"]
        },
    },
    "惠普 (HP)": {
        "暗影精灵 10 (i7-14650HX)": {
            "price": 8999.0, "status": True,
            "specs": ["i7-14650HX", "16G", "1T", "RTX 5060", "2.5K", "240Hz"]
        }
    },
    "自定义": {
        "手动输入机型": {
            "price": 0.0, "status": True,
            "specs": ["-", "-", "-", "-", "-", "-"]
        }
    }
}

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
