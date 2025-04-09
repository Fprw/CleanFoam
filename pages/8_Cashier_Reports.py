import streamlit as st
import pandas as pd
from utils.data_utils import load_csv
from utils.ui_helpers import show_header

show_header("تقارير الكاشير")

sales = load_csv("sales.csv")
expenses = load_csv("expenses_general.csv")
expenses_workers = load_csv("expenses_workers.csv")

report = st.selectbox("اختر نوع التقرير", ["التقرير اليومي", "تقرير العمال", "تقرير الغلة"])

if report == "التقرير اليومي":
    date = st.date_input("اختر التاريخ")
    df = sales[sales['date'] == str(date)]

    if df.empty:
        st.warning("لا توجد بيانات.")
    else:
        summary = df.groupby("worker_name").agg({"amount": "sum"}).reset_index()
        st.dataframe(summary)

        st.metric("إجمالي الكاش", df[df["payment_type"] == "كاش"]["amount"].sum())
        st.metric("إجمالي الشبكة", df[df["payment_type"] == "شبكة"]["amount"].sum())
        st.metric("الإجمالي", df["amount"].sum())

elif report == "تقرير العمال":
    start = st.date_input("من تاريخ")
    end = st.date_input("إلى تاريخ")
    df = sales[(sales["date"] >= str(start)) & (sales["date"] <= str(end))]
    exp_df = load_csv("expenses_workers.csv")

    table = []
    for worker in df["worker_name"].unique():
        total = df[df["worker_name"] == worker]["amount"].sum()
        withdraw = exp_df[exp_df["worker_name"] == worker]["amount"].sum()
        half = total / 2
        fee = 30
        remaining = half - fee - withdraw
        table.append([worker, total, withdraw, remaining])

    result = pd.DataFrame(table, columns=["العامل", "الإجمالي", "المسحوب", "الباقي"])
    st.dataframe(result)

elif report == "تقرير الغلة":
    mada = st.number_input("Mada", min_value=0.0)
    visa = st.number_input("Visa", min_value=0.0)
    master = st.number_input("MasterCard", min_value=0.0)
    cash = st.number_input("Cash", min_value=0.0)

    total = mada + visa + master + cash
    st.metric("المجموع الكلي", total)
