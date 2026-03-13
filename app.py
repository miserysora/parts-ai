import streamlit as st
import google.generativeai as genai
from PIL import Image

# 页面配置
st.set_page_config(page_title="机组零件识别系统", layout="centered", page_icon="🚢")

# --- 1. 初始化缓存 ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. 配置 AI 引擎 ---
try:
    # 尝试从 Secrets 获取 Key
    api_key = st.secrets["GEMINI_KEY"]
    # 使用 grpc 传输协议，这是解决 404 问题的最强补丁
    genai.configure(api_key=api_key, transport='grpc')
except Exception as e:
    st.error("🔑 未能读取到有效的 API Key。请检查 Streamlit 的 Secrets 设置。")

# --- 3. 界面头部 ---
st.title("🚢 燃油机零件智能识别系统")
st.markdown("""
通过 AI 技术快速识别 MTU、Cummins、Wartsila 及 Scania 发动机零件。
*若识别有误，请在下方手动校准，帮助系统学习。*
""")

# --- 4. 核心功能：拍照/上传 ---
uploaded_file = st.file_uploader("📸 第一步：上传或拍摄零件照片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # 显示图片
    img = Image.open(uploaded_file)
    st.image(img, caption="待识别零件预览", use_container_width=True)
    
    # 识别按钮
    if st.button("🚀 开始 AI 智能分析"):
        with st.spinner('正在连接全球专家库进行分析...'):
            # 定义提示词
            prompt = """你是一位精通燃油机工程的专家。请分析图片并提供：
            1. 零件准确名称
            2. 可能的 OEM 零件号
            3. 主要功能描述
            4. 推荐适用机型 (例如: MTU 4000 series, Cummins KTA50, Scania DC13)
            请用中文回答。"""
            
            try:
                # 尝试使用 Flash 模型
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("✅ 识别完成！")
                    st.markdown("### 🤖 AI 识别结果")
                    st.info(response.text)
                else:
                    st.warning("AI 响应成功但内容为空，请重试。")
            
            except Exception as e:
                # 最后的容错：显示具体错误提示
                st.error(f"⚠️ 识别过程遇到障碍：{str(e)}")
                st.info("💡 建议：检查 API Key 权限或尝试重新上传图片。")

# --- 5. 亮点功能：人工校准 (分享会加分项) ---
st.divider()
st.subheader("🛠️ 系统校准与人工反馈")
st.write("如果 AI 识别不准确，请录入正确数据以完善私有数据库：")

col1, col2 = st.columns(2)
with col1:
    c_name = st.text_input("正确零件名称", placeholder="例如：喷油嘴支架")
    c_no = st.text_input("正确零件号", placeholder="例如：0422 6517")
with col2:
    c_model = st.text_input("适用机型", placeholder="例如：MTU 2000")
    c_desc = st.text_area("备注信息", placeholder="补充功能或存储位置...", height=68)

if st.button("💾 提交校准并学习"):
    if c_name or c_no:
        # 保存到本轮缓存
        record = {
            "零件名": c_name,
            "零件号": c_no,
            "机型": c_model,
            "备注": c_desc
        }
        st.session_state.history.append(record)
        st.balloons() # 庆祝动画
        st.success("数据已成功记录至临时学习库！")
    else:
        st.warning("请至少输入零件名称或编号再提交。")

# --- 6. 展示校准结果 ---
if st.session_state.history:
    st.write("---")
    st.write("### 📋 本次会话校正清单")
    st.table(st.session_state.history)
