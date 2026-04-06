import streamlit as st
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

st.title("Function Tools Example")

if "light" not in st.session_state:
    st.session_state.light = 500

def get_current_light() -> int:
    """
    현재 조도 센서 값을 읽어옵니다.
    0은 완전한 어둠, 1023은 매우 밝음을 의미합니다.

    사용자가 환경 제어를 요청하면, 판단을 내리기 전에 반드시 이 함수를 먼저 호출하여 현재 밝기를 확인하세요.
    """
    current_value = st.session_state.light
    st.toast(f"AI가 현재 조도를 확인했습니다: {current_value}")
    return current_value

def control_blind(angle: int):
    """
    창문의 블라인드(서보모터) 각도를 조절하는 함수입니다.

    조도를 확인한 후, 빛이 강하면 각도를 높이고(120~180도), 어두우면 각도를 줄이세요(0~60)도.

    Args:
        angle: 0에서 180 사이의 정수 (0: 개방, 180: 차단)
    """
    st.toast(f"서보모터를 {angle}도로 회전합니다.")

st.session_state.light = st.slider("조도 센서 시뮬레이터", 0, 1023, 500)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

@st.cache_resource
def load_client():
    return genai.Client(api_key=GEMINI_API_KEY)

client = load_client()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config= types.GenerateContentConfig(
            tools=[get_current_light, control_blind],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False,
                maximum_remote_calls=5,
            )
        ),
    )

def render_part(part):
    if part.text:
        st.markdown(part.text)
    
    if part.function_call:
        with st.status(f"{part.function_call.name} 함수 호출 요청"):
            st.json(part.function_call.args)

    if part.function_response:
        with st.status(f"{part.function_response.name} 함수 호출 응답"):
            st.json(part.function_response.response)


for content in st.session_state.chat_session.get_history():
    with st.chat_message("ai" if content.role == "model" else "user"):
        for part in content.parts:
            render_part(part)

            
if prompt := st.chat_input("메시지를 입력하세요."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)
        for part in response.candidates[0].content.parts:
            render_part(part)

        st.rerun()
