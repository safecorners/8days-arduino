import streamlit as st
import pandas as pd
import serial
import json
import datetime
import time


st.title(":material/sensors: Sensor Monitoring")


if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["time", "light"]).set_index("time")


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


if ser and ser.is_open and ser.in_waiting > 0:
    try:
        message = ser.readline().decode('utf-8').strip()
        payload = json.loads(message)
        
        sensor_type = payload["type"]
        sensor_value = payload["value"]

        new_data = pd.DataFrame({
            "time": [datetime.datetime.now()],
            sensor_type: sensor_value,
        }).set_index("time")

        st.session_state.df = pd.concat([st.session_state.df, new_data])
    except Exception as e:
        st.sidebar.error(e)


st.header("실시간 데이터 흐름")
st.caption("최근 들어온 50개의 데이터를 실시간으로 보여줍니다.")
st.line_chart(st.session_state.df[-50:])


if not st.session_state.df.empty:
    m1, m2,m3,m4 = st.columns(4)
    m1.metric("현재", st.session_state.df["light"][-1:])
    m2.metric("평균", round(st.session_state.df["light"].mean()))
    m3.metric("최대", st.session_state.df["light"].max())
    m4.metric("최소", st.session_state.df["light"].min())


st.header("센서 값")
display_df = st.session_state.df.reset_index()
display_df = display_df[["light", "time"]]

st.dataframe(
    display_df.sort_values(by="time", ascending=False),
    hide_index=True,
)


time.sleep(0.1)
st.rerun()