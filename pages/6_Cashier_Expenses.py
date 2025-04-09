import streamlit as st
from utils.data_utils import append_csv, load_csv
from utils.ui_helpers import get_now

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("يرجى تسجيل الدخول أولاً.")
    st.stop()

if st.session_state.role != "cashier":
    st.error("غير مصرح لك بالدخول إلى هذه الصفحة.")
    st.stop()

st.title("المصروفات")

tab1, tab2 = st.tabs(["مصروفات عامة", "مصروفات عمال"])

with tab1:
    desc = st.text_input("الوصف")
    amt = st.number_input("المبلغ", min_value=1.0, key="gen_amt")
    if st.button("تسجيل كمصروف عام"):
        now = get_now()
        append_csv("expenses_general.csv", {
            "id": int(now.timestamp()),
            "amount": amt,
            "description": desc,
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "cashier": st.session_state.username
        })
        st.success("تم تسجيل المصروف العام.")

with tab2:
    workers = load_csv("workers.csv")["worker_name"].tolist()
    worker = st.selectbox("اختر العامل", workers)
    amt = st.number_input("المبلغ", min_value=1.0, key="w_amt")
    if st.button("تسجيل كمصروف للعامل"):
        now = get_now()
        append_csv("expenses_workers.csv", {
            "id": int(now.timestamp()),
            "worker_name": worker,
            "amount": amt,
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "cashier": st.session_state.username
        })
        st.success("تم تسجيل المصروف للعامل.")
