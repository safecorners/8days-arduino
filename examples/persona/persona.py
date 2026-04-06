import streamlit as st
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

st.title(":orange[:material/pets:] 고양이 챗봇")

st.caption("시스템 프롬프트를 추가해 페르소나를 입혀주세요.")

MODEL_NAME = "gemini-2.5-flash"

@st.cache_resource
def get_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("🔑API 키가 설정되지 않았습니다.")
        st.stop()

    return genai.Client(api_key=api_key)
    
client = get_client()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction="너는 야옹이야. 고양이처럼 말해야해. 야옹!"
        )
    )


for content in st.session_state.chat_session.get_history():
    with st.chat_message("assistant" if content.role == "model" else "user"):
        for part in content.parts:
            st.markdown(part.text)


if prompt := st.chat_input("고양이에게 물어보기"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)