import streamlit as st
import serial
import json


st.title(":material/precision_manufacturing: Servo Motor")


port = st.sidebar.text_input("Serial Port", value="COM3")

@st.cache_resource
def get_serial(port):
    try:
        return serial.Serial(port, 115200, timeout=1)
    
    except:
        return None
    

ser = get_serial(port)
if ser is not None:
    st.success(f"포트[{port}] 연결 성공!", icon=":material/usb:")
else:
    st.error(f"포트[{port}]을 찾을 수 없습니다.", icon=":material/usb_off:")


angle = st.slider("각도", 0, 180, 90, disabled=(ser is None))
payload = {
    "angle": angle,
}

if ser and ser.is_open:
    message = json.dumps(payload)
    ser.write(message.encode())

    st.subheader("JSON")
    st.code(message, language="json")