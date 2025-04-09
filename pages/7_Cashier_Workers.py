import streamlit as st
from utils.data_utils import load_csv, save_csv
import pandas as pd

st.title("إدارة العمال")

workers = load_csv("workers.csv")

st.subheader("إضافة عامل")
new_worker = st.text_input("اسم العامل الجديد")
if st.button("إضافة"):
    if new_worker and new_worker not in workers["worker_name"].values:
        workers = pd.concat([workers, pd.DataFrame([{"worker_name": new_worker}])], ignore_index=True)
        save_csv("workers.csv", workers)
        st.success("تمت الإضافة.")
        st.experimental_rerun()

st.subheader("حذف عامل")
if not workers.empty:
    to_delete = st.selectbox("اختر العامل", workers["worker_name"].tolist())
    if st.button("حذف العامل"):
        workers = workers[workers["worker_name"] != to_delete]
        save_csv("workers.csv", workers)
        st.success("تم الحذف.")
        st.experimental_rerun()
