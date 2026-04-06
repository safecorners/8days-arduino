import streamlit as st

st.session_state.angle = st.slider("각도", 0, 180, st.session_state.angle)