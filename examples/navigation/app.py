import streamlit as st


if "angle" not in st.session_state:
    st.session_state.angle = 90

pages = [
    st.Page("dashboard.py", title="대시보드", icon=":material/home:", default=True),
    st.Page("control.py", title="제어", icon=":material/sunny:"),
]

page = st.navigation(pages=pages)

st.title(f"{page.icon} {page.title}")

page.run()
