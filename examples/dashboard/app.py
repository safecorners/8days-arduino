import streamlit as st
import serial

from google import genai
from google.genai import types

from datetime import datetime
import time
import json

import os
from dotenv import load_dotenv

# =========================================================
# [구역 1] 환경 설정
# =========================================================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

st.set_page_config(page_title="8일간의 아두이노", layout="wide")


# =========================================================
# [구역 2] 리소스 및 외부 연결 관리
# =========================================================

@st.cache_resource
def get_ser(port):
    try:
        return serial.Serial(port, 115200, timeout=1)
    except:
        return None

@st.cache_resource
def get_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("🔑API 키가 설정되지 않았습니다.")
        st.stop()

    return genai.Client(api_key=api_key)

client = get_client()

port = st.sidebar.text_input("시리얼 포트", value="COM3")

st.session_state.ser = get_ser(port)

if st.session_state.ser is not None:
    st.sidebar.success(f"{port} 연결 성공!")
else:
    st.sidebar.error(f"{port}를 찾을 수 없습니다.")


# =========================================================
# [구역 3] 상태 초기화
# =========================================================

if "raw_data" not in st.session_state:
    st.session_state.raw_data = []

if "light" not in st.session_state:
    st.session_state.light = 500

if "angle" not in st.session_state:
    st.session_state.angle = 90

if "prev_angle" not in st.session_state:
    st.session_state.prev_angle = 90


# =========================================================
# [구역 4] AI 에이전트 및 도구(Tools) 정의
# =========================================================


def get_current_light() -> int:
    """
    현재 조도 센서 값을 읽어옵니다.
    0은 완전한 어둠, 1023은 매우 밝음을 의미합니다.
    """
    current_value = st.session_state.light
    st.toast(f"AI가 현재 조도를 확인했습니다: {current_value}")
    return current_value


def change_blind_angle(angle: int):
    """
    창문의 블라인드(서보모터) 각도를 조절하는 함수입니다.

    Args:
        angle: 0에서 180 사이의 정수 (0: 개방, 180: 차단)
    """
    ser = st.session_state.ser
    payload = {
        "type": "servo",
        "angle":angle,
    }
    message = json.dumps(payload) + "\n"
    
    if ser and ser.is_open:
        try:
            ser.write(message.encode())
            st.session_state.prev_angle = angle
            st.session_state.angle = angle

            st.toast(f"AI가 블라인드를 {angle}도로 조절했습니다.")
        except Exception as e:
            print(e)
    

def load_system_prompt(file_name):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_dir, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"{file_path}를 찾을 수 없습니다.")
        st.stop()


if "chat_session" not in st.session_state:
    system_prompt = load_system_prompt("system_prompt.md")
    tool_list = [get_current_light, change_blind_angle]
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config= types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools= tool_list,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False,
                maximum_remote_calls=5,
            )
        ),
    )


# =========================================================
# [구역 5] 데이터 수집
# =========================================================

def fetch_data():
    ser = st.session_state.ser
    if ser and ser.is_open and ser.in_waiting > 0:
        try:
            message = ser.readline().decode("utf-8").strip() 
            payload = json.loads(message)

            sensor_type = payload["type"]
            sensor_value = payload["value"]
            
            new_entry = {
                    "time": datetime.now(),
                    sensor_type: sensor_value,
            }

            st.session_state.raw_data.append(new_entry)

            if sensor_type == "light":
                st.session_state.light = sensor_value

        except Exception as e:
            print(e)

with st.sidebar:
    @st.fragment(run_every="1s")
    def collect_data():
        fetch_data()

        count = len(st.session_state.raw_data)
        st.status(f"수집된 데이터 개수: {count}")

    collect_data()
    

# =========================================================
# [구역 6] 페이지 내비게이션 및 앱 실행
# =========================================================

pages = [
    st.Page("dashboard.py", title="대시보드", icon=":material/dashboard:", default=True),
    st.Page("chatbot.py", title="챗봇", icon=":material/smart_toy:"),
    st.Page("control.py", title="수동 제어", icon=":material/adjust:"),
]

page = st.navigation(pages=pages)

st.title(f"{page.icon} {page.title}")

page.run()
