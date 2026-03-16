import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

st.set_page_config(page_title="مدرب القدرات الذكي", page_icon="🇸🇦")
st.title("🇸🇦 مدرب اختبار القدرات (GAT)")

# إدخال مفتاح API
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# --- الذاكرة: لحفظ سجل المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="""
        أنت مدرب خبير في اختبار القدرات السعودي (قياس). 
        مهامك:
        1. تقديم أسئلة في القسم الكمي (حساب، هندسة، جبر، مقارنات) واللفظي (تناظر، إكمال جمل، خطأ سياقي).
        2. الالتزام بمعايير "قياس": 4 خيارات (أ، ب، ج، د).
        3. عند تقديم الحل، اشرح "طريقة الحل السريعة" (تكتيكات الحل) لأن الوقت مهم.
        4. شجع الطالب بأسلوب محفز وودود.
        5. ابدأ دائماً باللغة العربية إلا إذا طلب الطالب غير ذلك.
        """)
    ]

# عرض سجل المحادثة
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# --- منطقة الإدخال والرد ---
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("من فضلك أضف مفتاح OpenAI API للاستمرار.")
        st.stop()

    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    # استدعاء النموذج
    model = ChatOpenAI(model="gpt-4o", temperature=0.5, api_key=openai_api_key)
    
    with st.chat_message("assistant"):
        response = model.invoke(st.session_state.messages)
        st.write(response.content)
        # إضافة رد البوت للسجل
        st.session_state.messages.append(AIMessage(content=response.content))
