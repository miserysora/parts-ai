import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 基础页面设置
st.set_page_config(page_title="零件识别系统", layout="centered")

# 2. 尝试初始化 AI（放在最前面，防止后面报错）
if 'history' not in st.session_state:
    st.session_state.history = []

# 获取 Secrets 里的 Key
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
    else:
        st.error("❌ 未在 Secrets 中找到 GEMINI_KEY")
except Exception as e:
    st.error(f"🔑 配置 Key 时出错: {e}")

# 3. 界面显示
st.title("🚢 燃油机零件智能识别系统")

uploaded_file = st.file_uploader("第一步：上传照片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="待识别零件", use_container_width=True)
    
    if st.button("🚀 开始 AI 识别"):
        with st.spinner('AI 正在分析...'):
            try:
                # 使用最标准的调用方式
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(["请识别图中的零件名称、功能和适用机型。", img])
                
                if response:
                    st.success("识别成功！")
                    st.markdown(response.text)
            except Exception as e:
                # 哪怕失败了，也要把具体的错误代码吐出来
                st.error(f"❌ 识别失败，错误详情：{e}")

# 4. 手动校准（即使 AI 坏了，这部分也要能用）
st.divider()
st.subheader("🛠️ 结果校正")
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("正确名称")
with c2:
    no = st.text_input("正确零件号")

if st.button("💾 提交数据"):
    if name or no:
        st.session_state.history.append({"零件名": name, "零件号": no})
        st.balloons()
    else:
        st.warning("请输入内容再提交")

if st.session_state.history:
    st.table(st.session_state.history)
