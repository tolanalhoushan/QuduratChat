import streamlit as st
from langchain_openai import ChatOpenAI # الطريقة الحديثة للاستيراد
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

st.set_page_config(page_title="مدرب القدرات الذكي", page_icon="🇸🇦")
st.title("🇸🇦 مدرب اختبار القدرات (GAT)")

# قراءة المفتاح من Secrets بدلاً من واجهة المستخدم
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("خطأ: لم يتم العثور على مفتاح API في إعدادات Secrets.")
    st.stop()

# باقي الكود كما هو...
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="أنت مدرب خبير في اختبار القدرات السعودي...")
    ]

# (تكملة الكود الذي يعرض الرسائل ويستدعي النموذج)
if prompt := st.chat_input():
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    # استخدام المفتاح المسحوب من Secrets
    model = ChatOpenAI(model="gpt-4o", temperature=0.5, api_key=openai_api_key)
    
    with st.chat_message("assistant"):
        response = model.invoke(st.session_state.messages)
        st.write(response.content)
        st.session_state.messages.append(AIMessage(content=response.content))
