import streamlit as st
import pandas as pd
import json
import os

# --- 1. 数据加载模块 ---
def load_data():
    if os.path.exists("laptops.json"):
        with open("laptops.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_tips():
    if os.path.exists("tips.json"):
        with open("tips.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

MODEL_DB = load_data()
TIPS_DB = load_tips()

# --- 2. 逻辑计算模块 (已修改: 增加 has_subsidy 判断) ---
def calculate_subsidy(price, has_subsidy):
    """2026年国补标准：如果有补贴，享15%补贴(最高1500元)；否则原价"""
    if has_subsidy:
        return price - min(price * 0.15, 1500)
    return price

# --- 3. Streamlit UI ---
st.set_page_config(page_title="大学生选购助手 2026", layout="wide")
st.title("🎓 大学生电脑选购智能推荐 (2026 国补版)")

# 将输入框从 sidebar 移到主体部分，采用两列布局
st.subheader("🔍 你的需求定制")
col_input1, col_input2 = st.columns(2)

with col_input1:
    major_type = st.selectbox("选择你的学科类别", 
        [ "文管/通用 (办公/刷课)", "传媒/艺术 (剪辑/设计)", "计算机/软件 (编程/虚拟机)", "理工科 (仿真/建模/渲染)"])
    budget = st.slider("你的预算上限 (最终到手价)", 4000, 16000, 6000)

with col_input2:
    st.write("---") # 简单的视觉对齐
    gaming_need = st.checkbox("有重度游戏需求 (3A大作)")
    portability_first = st.checkbox("优先考虑便携性 (常带去图书馆)")
    only_subsidy = st.checkbox("只显示参加国补的机型") # 新增选项

# --- 4. 核心功能：基于建议库的智能贴士 ---
if TIPS_DB:
    with st.expander("✨ 针对你专业的选购小贴士", expanded=True):
        # 自动匹配当前学科的建议
        scenario_tip = TIPS_DB["scenarios"].get(major_type, "选择专业以查看定制建议")
        st.info(scenario_tip)
        
        # 动态解析 CPU 类型
        st.caption("🔍 **快速避坑：CPU选购** " + " | ".join([
            "**HX系列**: 性能强劲但必须插电，不插电性能缩水",
            "**Ultra V/H**: 2026主流选Ultra，续航翻倍且支持AI NPU",
            "**Ryzen**: 买新不买旧，选8000/9000系列兼顾核显游戏"
        ]))

# --- 5. 过滤与推荐算法 (已修改: 整合补贴状态逻辑) ---
st.subheader("💡 为你匹配的机型")

recommendations = []
for brand, models in MODEL_DB.items():
    if brand == "自定义": continue
    
    for name, data in models.items():
        if any(kw in name for kw in ["一体机", "AIO", "台式"]): continue
        
        price = data["price"]
        # 读取 JSON 中的 status 字段，如果没填默认当做 False
        has_subsidy = data.get("status", False) 
        
        # 如果用户勾选了“只看国补”，且这台机器没有，直接跳过
        if only_subsidy and not has_subsidy:
            continue
            
        cpu, ram, ssd, gpu, screen, refresh = data["specs"]
        final_price = calculate_subsidy(price, has_subsidy) # 计算最终价格
        
        # --- 1. 基础属性解析 ---
        ram_val = int(''.join(filter(str.isdigit, ram))) 
        is_2k_plus = any(x in screen.upper() for x in ["2K", "2.5K", "2.8K", "3K", "4K"]) or ("2" in screen and "x" in screen)

        # --- 2. 性能标签化 ---
        is_gaming_perf = "5060" in gpu or "5070" in gpu or "3050" in gpu or "4050" in gpu
        is_high_cpu = any(x in cpu for x in ["Ultra 5 2", "Ultra 5 3", "Ultra 7", "Core 7", "Ultra 9", "Ryzen 7", "Ryzen 9", "i7", "i9"])
        is_strong_igpu = any(x in gpu for x in ["Arc", "Radeon 780M", "140V", "核显"])
        
        is_creative_high_spec = (ram_val >= 32 and is_2k_plus and (is_high_cpu or is_strong_igpu))

        # --- 3. 匹配逻辑判定 ---
        is_match = True
        
        # 预算过滤
        if final_price > budget:
            is_match = False
            
        # 传媒/艺术 (剪辑/设计) 专项过滤
        elif "传媒" in major_type:
            if not is_2k_plus:
                is_match = False
            elif not (is_gaming_perf or is_creative_high_spec):
                is_match = False
                
        # 计算机专业过滤
        elif "计算机" in major_type:
            if not (is_gaming_perf or is_high_cpu or ram_val >= 32):
                is_match = False
        
        # 理工科和重度游戏过滤
        if (gaming_need or "理工" in major_type) and not is_gaming_perf:
            is_match = False
            
        # 便携性过滤
        if portability_first and any(kw in name for kw in [
            "拯救者", "精灵", "极光X", "极光", "蛟龙", "潮玩版", "耀世", "旷世",
            "苍龙"
            ]):
            is_match = False

        if is_match:
            recommendations.append({
                "品牌": brand,
                "型号": name,
                "原价": price,
                "国补状态": "✅ 参加" if has_subsidy else "❌ 不参加", # 新增展示列
                "最终到手价": final_price,
                "核心配置": f"{cpu} | {ram} | {gpu} | {ssd}",
                "屏幕": f"{screen} / {refresh}"
            })
            
# --- 6. 结果展示 (已修改: 更新字段名) ---
if recommendations:
    df = pd.DataFrame(recommendations).sort_values(by="最终到手价", ascending=True)
    
    # 格式化输出
    df_display = df.copy()
    df_display["原价"] = df_display["原价"].apply(lambda x: f"¥{x:.0f}")
    df_display["最终到手价"] = df_display["最终到手价"].apply(lambda x: f"¥{x:.2f}")
    
    st.table(df_display.reset_index(drop=True))
    
    # 额外反馈
    best_deal = df.iloc[0]
    st.success(f"✅ 最省钱方案：**{best_deal['型号']}**，最终到手价仅需 **¥{best_deal['最终到手价']:.2f}**")
else:
    st.warning("☹️ 当前预算下未找到完美匹配，建议稍微调高预算或放宽便携性要求。")

st.info("💡 提示：以上建议仅供参考。部分机型价格浮动，如需了解或选购其他机型，请到店咨询。")

# --- 7. 底部百科导航 ---
st.divider()  # 添加一条分割线
st.markdown("### 📚 其他功能")

# 使用 columns 让链接横向排布
col_wiki1, col_wiki2, col_wiki3, col_wiki4 = st.columns(4)

with col_wiki1:
    st.page_link("pages/1_国补计算器.py", label="国补计算器", icon="📱")

with col_wiki2:
    st.page_link("pages/2_CPU性能百科.py", label="CPU性能百科", icon="🔍")

with col_wiki3:
    st.page_link("pages/3_内存性能百科.py", label="内存性能百科", icon="🔍")

with col_wiki4:
    st.page_link("pages/4_显卡性能百科.py", label="显卡性能百科", icon="🔍")
#收起侧边栏
st.set_page_config(
    page_title="电脑选购助手 2026", 
    layout="wide",
    initial_sidebar_state="collapsed" # 默认收起侧边栏
)
# --- 页面底部：店铺信息与地图导向 ---
st.divider() # 添加一条精美的分割线

# 创建三列布局，让地址居中或靠左显示
footer_left, footer_mid, footer_right = st.columns([2, 1, 1])

with footer_left:
    st.markdown("### 📍 店铺地址")
    st.write("🏠 **地址**：黔西南布依族苗族自治州 兴义市 神奇东路1号 泰鑫科技数码城 2楼")
    
    # 使用 Markdown 语法创建超链接
    # 将引号内的 URL 替换为百度地图或高德地图的分享链接
    map_url_1 = "https://surl.amap.com/4qgDXUmc5lM" 
    st.markdown(f"🔗 [点击此处在地图中查看 (高德地图)]({map_url_1})")

    map_url_2 = "https://j.map.baidu.com/56/51iM" 
    st.markdown(f"🔗 [点击此处在地图中查看 (百度地图)]({map_url_2})")

with footer_mid:
    st.markdown("### 📞 联系方式")
    st.write("客服电话：0859-3227511")
    st.write("营业时间：09:00 - 18:00")

#with footer_right:
 #   st.caption("扫码关注公众号获取更多补贴资讯")
    # 如果你有二维码图片，可以使用 st.image("qrcode.png", width=100)
