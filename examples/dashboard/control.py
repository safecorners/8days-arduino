import streamlit as st
import json

ser = st.session_state.ser

angle = st.slider("각도", 0, 180, st.session_state.angle, disabled=(ser is None))


if angle != st.session_state.prev_angle:
    payload = {
        "type": "servo",
        "angle":angle,
    }
    message = json.dumps(payload) + "\n"

    if ser and ser.is_open:
        ser.write(message.encode())
        st.session_state.prev_angle = angle
        st.session_state.angle = angle

with st.expander("JSON"):
    current_payload = {
        "type": "servo",
        "angle":angle,
    }
    st.code(json.dumps(current_payload, indent=2), language="json")
