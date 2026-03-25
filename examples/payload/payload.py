import streamlit as st
import serial
import json


st.title("Led Switch With JSON")


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


msg = ""
if st.button("On",
             icon=":material/lightbulb:",
             use_container_width=True,
             disabled=(ser is None),
             ):
    payload = {"led": "on"}
    msg = json.dumps(payload) + "\n"
    ser.write(msg.encode())
    
if st.button("Off",
             icon=":material/power_off:",
             use_container_width=True,
             disabled=(ser is None),
             ):
    payload = {"led": "off"}
    msg = json.dumps(payload) + "\n"
    ser.write(msg.encode())


if ser and ser.is_open:
    st.subheader("JSON")
    st.code(msg, language="json")