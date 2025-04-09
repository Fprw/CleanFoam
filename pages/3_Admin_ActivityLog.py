import streamlit as st
import pandas as pd
from utils.data_utils import load_csv
from utils.ui_helpers import show_header

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("يرجى تسجيل الدخول أولاً.")
    st.stop()

if st.session_state.role != "admin":
    st.error("غير مصرح لك بالدخول إلى هذه الصفحة.")
    st.stop()

show_header("سجل النشاطات")

log = load_csv("activity_log.csv")

if log.empty:
    st.info("لا توجد نشاطات مسجلة.")
else:
    log = log.sort_values(by="timestamp", ascending=False)
    st.dataframe(log, use_container_width=True)

    if st.checkbox("تصفية حسب المستخدم"):
        users = log["username"].unique().tolist()
        selected_user = st.selectbox("اختر المستخدم", users)
        st.dataframe(log[log["username"] == selected_user], use_container_width=True)

    if st.checkbox("تصفية حسب نوع النشاط"):
        actions = log["action"].unique().tolist()
        selected_action = st.selectbox("اختر النشاط", actions)
        st.dataframe(log[log["action"] == selected_action], use_container_width=True)
