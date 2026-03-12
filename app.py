import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="机组零件识别", layout="centered")

# 配置你的 API Key
genai.configure(api_key="AIzaSyBACiBy8Z7pkpthjIsz_IgLNdvlljuhkn4")

st.title("🚢 燃油机零件智能识别系统")
st.write("当前支持：MTU, Cummins, Wartsila, Scania")

图片上传
uploaded_file = st.file_uploader("第一步：上传/拍摄零件照片", type=["jpg", "png", "jpeg"])

if uploaded_file:
img = Image.open(uploaded_file)

st.image(img, caption="待识别零件", use_container_width=True)
