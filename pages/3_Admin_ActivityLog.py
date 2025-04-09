import streamlit as st
import pandas as pd
from utils.data_utils import load_csv
from utils.ui_helpers import show_header

show_header("سجل النشاطات")

log = load_csv("activity_log.csv")

if log.empty:
    st.info("لا توجد أي نشاطات مسجلة حتى الآن.")
else:
    log = log.sort_values(by="timestamp", ascending=False)
    st.dataframe(log, use_container_width=True)

    if st.checkbox("تصفية حسب المستخدم"):
        users = log["username"].unique().tolist()
        selected = st.selectbox("اختر المستخدم", users)
        st.dataframe(log[log["username"] == selected], use_container_width=True)

    if st.checkbox("تصفية حسب نوع النشاط"):
        actions = log["action"].unique().tolist()
        selected_action = st.selectbox("اختر النشاط", actions)
        st.dataframe(log[log["action"] == selected_action], use_container_width=True)
