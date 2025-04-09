import streamlit as st
from datetime import datetime
import pandas as pd
from utils.data_utils import append_csv, load_csv
from utils.ui_helpers import get_now

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("يرجى تسجيل الدخول أولاً.")
    st.stop()

if st.session_state.role != "cashier":
    st.error("غير مصرح لك بالدخول إلى هذه الصفحة.")
    st.stop()

st.title("نقطة البيع")

workers = load_csv("workers.csv")["worker_name"].tolist()

if "last_invoice" not in st.session_state:
    st.session_state.last_invoice = None

invoice_id = int(datetime.now().timestamp())

worker = st.selectbox("اسم العامل", workers)
amount = st.number_input("المبلغ", min_value=1.0)
payment_type = st.radio("نوع الدفع", ["كاش", "شبكة"])

if st.button("بيع"):
    now = get_now()
    data = {
        "invoice_id": invoice_id,
        "worker_name": worker,
        "amount": amount,
        "payment_type": payment_type,
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "cashier": st.session_state.username
    }
    append_csv("sales.csv", data)
    st.session_state.last_invoice = data
    st.success("تم تسجيل الفاتورة بنجاح.")
    st.audio("static/alert_sound.mp3")

if st.session_state.last_invoice:
    with st.expander("عرض الفاتورة السابقة"):
        st.json(st.session_state.last_invoice)
