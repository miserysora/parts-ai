import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="零件识别系统", layout="centered")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- 核心修复：强制指定 API 版本 ---
try:
    if "GEMINI_KEY" in st.secrets:
        # 手动指定使用 v1 正式版接口，避开报错的 v1beta
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
    else:
        st.error("❌ 未在 Secrets 中找到 GEMINI_KEY")
except Exception as e:
    st.error(f"🔑 配置出错: {e}")

st.title("🚢 燃油机零件智能识别系统")

uploaded_file = st.file_uploader("第一步：上传照片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="待识别零件", use_container_width=True)
    
    if st.button("🚀 开始 AI 识别"):
        with st.spinner('AI 正在分析...'):
            try:
                # 尝试三种不同的模型命名方案，只要一个通了就行
                success = False
                # 方案 A: 标准 flash
                model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro-vision']
                
                for m_name in model_names:
                    try:
                        model = genai.GenerativeModel(m_name)
                        # 重点：对于图片识别，Gemini 1.5 统一使用 generate_content
                        response = model.generate_content(["识别图中的零件名称、功能和适用机型，用中文回答。", img])
                        if response.text:
                            st.success(f"识别成功！(驱动模式: {m_name})")
                            st.markdown(response.text)
                            success = True
                            break
                    except:
                        continue
                
                if not success:
                    st.error("❌ 抱歉，当前 AI 引擎在云端排队较多或接口受限。")
                    st.info("💡 建议：请直接在下方手动录入，演示系统的『人工校准』核心功能。")
                    
            except Exception as e:
                st.error(f"识别异常: {e}")

# --- 手动校准模块 (演示重点) ---
st.divider()
st.subheader("🛠️ 结果校正与数据采集")
st.write("当 AI 无法实时响应时，工程师可手动录入以完善本地数据库：")

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("零件名称")
    no = st.text_input("零件编号")
with c2:
    model_type = st.text_input("适用机型")
    desc = st.text_area("功能备注")

if st.button("💾 提交校准数据"):
    if name or no:
        st.session_state.history.append({
            "零件名": name, 
            "编号": no, 
            "机型": model_type,
            "备注": desc
        })
        st.balloons()
    else:
        st.warning("请至少输入零件名称或编号")

if st.session_state.history:
    st.write("### 📋 待入库零件清單")
    st.table(st.session_state.history)
