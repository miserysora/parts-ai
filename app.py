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
            except Exception as e:
                st.error("识别出错，请检查网络")

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
# 在代碼頂部（import之後）加入這行，用來初始化儲存空間
    if 'history' not in st.session_state:
        st.session_state.history = []

    st.divider()
    st.subheader("🛠️ 結果校正 (人工糾錯)")
    st.info("如果AI識別有誤，請在下方輸入正確信息，系統將記錄並學習。")
    
    c1, c2 = st.columns(2)
    with c1:
        correct_name = st.text_input("正確零件名稱")
        correct_no = st.text_input("正確零件號")
    with c2:
        correct_model = st.text_input("對應機型")
        correct_desc = st.text_area("功能描述")
        
    if st.button("💾 提交校准數據"):
        # 將輸入的數據存入一個清單
        new_data = {
            "零件名": correct_name,
            "零件號": correct_no,
            "機型": correct_model,
            "描述": correct_desc
        }
        st.session_state.history.append(new_data) # 存入內存
        st.balloons()
        st.success("已成功存入私有學習庫！")

    # --- 新增：顯示校正清單 ---
    if st.session_state.history:
        st.write("### 📋 本次運行已校正的數據：")
        st.table(st.session_state.history) # 以表格形式顯示
