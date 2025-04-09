import streamlit as st
from utils.ui_helpers import show_header, get_now
import pandas as pd
from utils.data_utils import load_csv

show_header("لوحة تحكم الأدمن")

sales = load_csv("sales.csv")
expenses = load_csv("expenses_general.csv")
now = get_now()
today = now.strftime("%Y-%m-%d")

today_sales = sales[sales['date'] == today]
today_expenses = expenses[expenses['date'] == today]

col1, col2, col3 = st.columns(3)
col1.metric("إجمالي الكاش", f"{today_sales[today_sales['payment_type'] == 'كاش']['amount'].sum():,.2f}")
col2.metric("إجمالي الشبكة", f"{today_sales[today_sales['payment_type'] == 'شبكة']['amount'].sum():,.2f}")
col3.metric("عدد العمليات", len(today_sales))

st.markdown("---")

if st.button("عرض اليوم السابق"):
    st.session_state.selected_date = (now - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    st.experimental_set_query_params(view="reports")

if st.button("عرض اليوم الذي قبله"):
    st.session_state.selected_date = (now - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
    st.experimental_set_query_params(view="reports")
