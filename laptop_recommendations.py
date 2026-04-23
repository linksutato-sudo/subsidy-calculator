import streamlit as st
import pandas as pd

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
        "拯救者 Y7000 IRX10 (i7-14650HX/512G)": {
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
            "specs": ["Ultra 5 336H", "32GB", "1TB", "Intel Graphics", "2.8K", "120Hz OLED"]
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
        },
        '光影精灵 11 悦龙版 (15")': {
            "price": 9299.0,  
            "status": True,
            "specs": ["Ryzen 7 H 255", "24GB", "1TB", "RTX 5060 8G", "1080P FHD", "144Hz"]
        },
        "OmniBook 3 星book 16": {
            "price": 7999.0,
            "status": True,
            "specs": ["Core 7-240H", "32G DDR5", "1TB", "Intel(R) Graphics", "2.5K", "240Hz"]
        },
        "OmniBook 7 (星Book Pro 16)": {
            "price": 6699.0,
            "status": True,
            "specs": ["Core 7-240H", "32G DDR5", "1TB", "Intel(R) Graphics", "2.5K", "240Hz"]
        },
        "OmniBook 7 (星Book Pro 14)": {
            "price": 5599.0,
            "status": True,
            "specs": ["Core 5-220H", "16G", "1TB", "Intel(R) Graphics", "2.2K", "60Hz"]
        },
        "Pavilion 星Book Pro 14 Plus": {
            "price": 6499.0,
            "status": True,
            "specs": ["Ultra 5 125H", "32G", "1TB", "Intel(R) Arc(TM) Graphics", "2.5K", "120Hz"]
        },
        "星Book 15": {
            "price": 4999.0,
            "status": True,
            "specs": ["Ultra 5 125H", "16G", "512G", "Intel(R) Arc(TM) Graphics", "1080P FHD", "60Hz"]
        },
    },
    "自定义": {
        "手动输入机型": {
            "price": 0.0, "status": True,
            "specs": ["-", "-", "-", "-", "-", "-"]
        }
    }
}

def calculate_subsidy(price):
    """计算2026年国补后的价格"""
    subsidy_amount = min(price * 0.15, 1500)
    return price - subsidy_amount

# --- Streamlit UI 界面 ---
st.set_page_config(page_title="大学生选购助手 2026", layout="wide")
st.title("🎓 大学生电脑选购智能推荐 (2026 国补版)")

# 侧边栏：用户需求输入
with st.sidebar:
    st.header("🔍 你的需求")
    major_type = st.selectbox("选择你的学科类别", 
        ["理工科 (仿真/建模/渲染)", "计算机/软件 (编程/虚拟机)", "传媒/艺术 (剪辑/设计)", "文管/通用 (办公/刷课)"])
    
    # 修改此处：明确是补贴后预算
    budget = st.slider("你的预算范围 (国补后价格)", 3000, 14000, 7000)
    
    gaming_need = st.checkbox("有重度游戏需求 (3A大作)")
    portability_first = st.checkbox("优先考虑便携性 (经常带去图书馆)")

# 逻辑过滤
st.subheader("💡 为你匹配的机型")

recommendations = []
for brand, models in MODEL_DB.items():
    for name, data in models.items():
        # 1. 提取数据 (修复之前的解包报错)
        price = data["price"]
        has_subsidy = data["status"]
        cpu, ram, ssd, gpu, screen, refresh = data["specs"]
        
        
       
        
        # 如果补贴后的价格超过了用户的预算，则排除
        if final_price > budget: 
            is_match = False
        
        # 4. 其他性能强度判断
        #is_high_perf = "5060" in gpu or "i7" in cpu or "i9" in cpu or "R9" in cpu
        # --- 修改后的匹配逻辑 ---

        # 1. 定义什么是“发烧级性能”（适合重度 3A 游戏和理工科建模）
        is_gaming_perf = "5060" in gpu or "5070" in gpu
        
        # 2. 定义什么是“全能级性能”（适合传媒剪辑、设计，包含新款 Ultra 处理器）
        is_design_perf = is_gaming_perf or "Ultra 7" in cpu or "Ultra 9" in cpu or "Ryzen 7" in cpu or "Ryzen 9" in cpu
        
        # 3. 针对不同专业实施过滤
        is_match = True
        
        # 预算过滤
        if final_price > budget: is_match = False
        
        # 性能过滤逻辑
        if gaming_need or "理工" in major_type:
            # 游戏和理工科必须要是发烧级显卡
            if not is_gaming_perf: is_match = False
        elif "传媒" in major_type:
            # 传媒设计只需要达到“全能级”即可（包含高性能轻薄本）
            if not is_design_perf: is_match = False
        
        # 便携性过滤
        if portability_first:
            # 如果勾选了便携，排除掉笨重的游戏本系列
            if "拯救者" in name or "暗影精灵" in name or "光影精灵" in name: 
                is_match = False
        # 性能判断结束
        if gaming_need or "理工" in major_type or "传媒" in major_type:
            if not is_high_perf: is_match = False
            
        if portability_first:
            if "拯救者" in name or "暗影精灵" in name: is_match = False

        if is_match:
            recommendations.append({
                "品牌": brand,
                "型号": name,
                "原价": f"¥{price}",
                "国补后": f"¥{final_price:.2f}",
                "核心配置": f"{cpu} | {ram} | {gpu}",
            })
# --- 结果显示区域 ---
if recommendations:
    df = pd.DataFrame(recommendations)
    # 使用 st.dataframe 可以让表格支持鼠标滚动和排序，体验更好
    st.table(df) 
else:
    st.warning("暂无完全匹配机型，建议适当增加预算或放宽要求。")

st.info("💡 提示：2026年国补单件最高省1500元，以上价格仅供参考，以店面实际结账为准。")
