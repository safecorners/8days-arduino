import streamlit as st
import serial


st.title("LED Switch")


port = st.sidebar.text_input("Serial Port", value="COM3")

@st.cache_resource
def get_serial(port_name):
    try:
        return serial.Serial(port_name, 115200, timeout=1)
    except:
        return None


ser = get_serial(port)
if ser is not None:
    st.success(f"포트[{port}] 연결 성공!", icon=":material/usb:")
else:
    st.error(f"포트[{port}]을 찾을 수 없습니다.", icon=":material/usb_off:")


if ser is not None:
    if st.button("ON"):
        ser.write(b'1')

    if st.button("OFF"):
        ser.write(b'0')