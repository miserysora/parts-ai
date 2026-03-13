import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="机组零件识别", layout="centered")

# 初始化历史记录（防止手动校准数据丢失）
if 'history' not in st.session_state:
    st.session_state.history = []

# 安全读取 API Key
# 请确保你在 Streamlit Cloud 的 Settings -> Secrets 里设置了 GEMINI_KEY
try:
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
except:
    st.warning("⚠️ 未在 Secrets 中找到 GEMINI_KEY，尝试从代码读取（不建议公开）")
    # 如果你还没设 Secrets，可以在下面这行临时填入，但别传到 GitHub 公开仓库
    # genai.configure(api_key="你的KEY")

st.title("🚢 燃油机零件智能识别系统")
st.write("当前支持：MTU, Cummins, Wartsila, Scania")

uploaded_file = st.file_uploader("第一步：上传/拍摄零件照片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="待识别零件", use_container_width=True)
    
    if st.button("🚀 开始 AI 识别"):
        model = genai.GenerativeModel('gemini-1.5-pro')
        with st.spinner('AI 专家正在分析中...'):
            prompt = "你是一位工业发动机专家。请识别图中的零件，给出：1.名称 2.可能零件号 3.功能 4.适用机型(如MTU 4000, Cummins KTA50)。"
            try:
                # 这里是核心识别代码
                response = model.generate_content([prompt, img])
                st.success("识别成功！")
                st.markdown(response.text)
            except Exception as e:
                # 如果失败，这里会显示具体的报错原因
                st.error(f"❌ AI 识别失败。具体原因：{e}")
                st.info("提示：如果是 403 错误，通常是 API Key 失效或地区限制。")

    st.divider()
    st.subheader("🛠️ 结果校正 (人工纠错)")
    
    c1, c2 = st.columns(2)
    with c1:
        correct_name = st.text_input("正确零件名称")
        correct_no = st.text_input("正确零件号")
    with c2:
        correct_model = st.text_input("对应机型")
        correct_desc = st.text_area("功能描述")
        
    if st.button("💾 提交校准数据"):
        if correct_name or correct_no:
            new_data = {"零件名": correct_name, "零件号": correct_no, "机型": correct_model, "描述": correct_desc}
            st.session_state.history.append(new_data)
            st.balloons()
            st.success("已成功记录！")
        else:
            st.warning("请至少填写零件名称或编号。")

    # 显示校正历史
    if st.session_state.history:
        st.write("### 📋 本次运行已校正的数据：")
        st.table(st.session_state.history)


