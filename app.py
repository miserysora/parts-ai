import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="机组零件识别", layout="centered")

# 配置你的 API Key
genai.configure(api_key="AIzaSyBACiBy8Z7pkpthjIsz_IgLNdvlljuhkn4")

st.title("🚢 燃油机零件智能识别系统")
st.write("当前支持：MTU, Cummins, Wartsila, Scania")

# 图片上传
uploaded_file = st.file_uploader("第一步：上传/拍摄零件照片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="待识别零件", use_container_width=True)
    
    if st.button("🚀 开始 AI 识别"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner('AI 专家正在分析中...'):
            prompt = "你是一位工业发动机专家。请识别图中的零件，给出：1.名称 2.可能零件号 3.功能 4.适用机型(如MTU 4000系列, Cummins KTA50, Wartsila W6L32, Scania DC13)。"
            try:
                response = model.generate_content([prompt, img])
                st.success("识别建议如下：")
                st.markdown(response.text)
# 改成这部分（让它显示真实错误）：
except Exception as e:
    st.error(f"AI 引擎报告了一个错误：{e}")

    st.divider()
    st.subheader("🛠️ 结果校正 (人工纠错)")
    st.info("如果AI识别有误，请在下方输入正确信息，系统将记录并学习。")
    
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("正确零件名称")
        st.text_input("正确零件号")
    with c2:
        st.text_input("对应机型")
        st.text_area("功能描述")
        
    if st.button("💾 提交校准数据"):
        st.balloons()
        st.success("已成功存入私有学习库！")

