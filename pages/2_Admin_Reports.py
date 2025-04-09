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

show_header("تقارير الأدمن")

sales = load_csv("sales.csv")
expenses = load_csv("expenses_general.csv")
expenses_workers = load_csv("expenses_workers.csv")

report_type = st.selectbox("اختر نوع التقرير", [
    "تقرير يومي", 
    "تقرير مخصص", 
    "تقرير المصروفات", 
    "تقرير العمال", 
    "مقارنة بين فترتين"
])

if report_type == "تقرير يومي":
    date = st.date_input("اختر التاريخ")
    df = sales[sales['date'] == str(date)]

    st.subheader(f"تقرير يوم {date}")
    st.dataframe(df)
    st.metric("إجمالي الكاش", df[df["payment_type"] == "كاش"]["amount"].sum())
    st.metric("إجمالي الشبكة", df[df["payment_type"] == "شبكة"]["amount"].sum())
    st.metric("الإجمالي", df["amount"].sum())

elif report_type == "تقرير مخصص":
    col1, col2 = st.columns(2)
    start = col1.date_input("من تاريخ")
    end = col2.date_input("إلى تاريخ")
    df = sales[(sales['date'] >= str(start)) & (sales['date'] <= str(end))]

    st.subheader(f"من {start} إلى {end}")
    st.metric("إجمالي الكاش", df[df["payment_type"] == "كاش"]["amount"].sum())
    st.metric("إجمالي الشبكة", df[df["payment_type"] == "شبكة"]["amount"].sum())
    st.metric("الإجمالي", df["amount"].sum())
    st.dataframe(df)

elif report_type == "تقرير المصروفات":
    col1, col2 = st.columns(2)
    start = col1.date_input("من تاريخ", key="exp1")
    end = col2.date_input("إلى تاريخ", key="exp2")
    all_exp = pd.concat([expenses, expenses_workers])
    df = all_exp[(all_exp['date'] >= str(start)) & (all_exp['date'] <= str(end))]
    st.subheader(f"المصروفات من {start} إلى {end}")
    st.dataframe(df)

elif report_type == "تقرير العمال":
    start = st.date_input("من تاريخ", key="w1")
    end = st.date_input("إلى تاريخ", key="w2")
    workers = sorted(sales["worker_name"].unique())
    worker_choice = st.selectbox("اختر عامل", ["كل العمال"] + workers)
    df = sales[(sales['date'] >= str(start)) & (sales['date'] <= str(end))]

    if worker_choice != "كل العمال":
        df = df[df["worker_name"] == worker_choice]

    grouped = df.groupby("worker_name").agg({"amount": "sum"}).reset_index()
    st.dataframe(grouped)

elif report_type == "مقارنة بين فترتين":
    col1, col2 = st.columns(2)
    start1 = col1.date_input("من (الفترة 1)")
    end1 = col1.date_input("إلى (الفترة 1)")
    start2 = col2.date_input("من (الفترة 2)")
    end2 = col2.date_input("إلى (الفترة 2)")

    df1 = sales[(sales['date'] >= str(start1)) & (sales['date'] <= str(end1))]
    df2 = sales[(sales['date'] >= str(start2)) & (sales['date'] <= str(end2))]

    st.subheader("الفترة 1")
    st.metric("كاش", df1[df1["payment_type"] == "كاش"]["amount"].sum())
    st.metric("شبكة", df1[df1["payment_type"] == "شبكة"]["amount"].sum())

    st.subheader("الفترة 2")
    st.metric("كاش", df2[df2["payment_type"] == "كاش"]["amount"].sum())
    st.metric("شبكة", df2[df2["payment_type"] == "شبكة"]["amount"].sum())
