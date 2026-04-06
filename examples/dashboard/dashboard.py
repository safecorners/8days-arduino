from datetime import datetime

import streamlit as st
import pandas as pd


@st.fragment(run_every="1s")
def display_data():

    if not st.session_state.raw_data:
        return
    
    df = pd.DataFrame(st.session_state.raw_data)
    
    if "time" in df.columns:
        df = df.set_index("time")
    
    if "light" in df.columns:
        df["light_ma"] = df["light"].rolling(window=5).mean()

    display_df = df.tail(60)
    st.line_chart(display_df[["light", "light_ma"]])
    
    current_value = display_df["light"].values[-1]
    max_value = display_df["light"].max()
    min_value = display_df["light"].min()
    avg_value = display_df["light"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("현재", current_value)
    col2.metric("최대", max_value)
    col3.metric("최소", min_value)
    col4.metric("평균", f"{avg_value:0.0f}")

    with st.expander("원본 데이터 보기"):
        st.dataframe(df.sort_index(ascending=False))

display_data()