import streamlit as st
import pandas as pd
from utils.data_utils import load_csv
from utils.ui_helpers import get_now, show_header

st.set_page_config(page_title="واجهة الكاشير - CleanFoam", page_icon="🧼", layout="wide")

if "authenticated" not in st.session_state or not st.session_state.authenticated or st.session_state.role != "cashier":
    st.error("غير مصرح لك بالوصول إلى هذه الصفحة.")
    st.stop()

show_header("واجهة الكاشير")

menu = st.sidebar.radio("القائمة", [
    "نقطة البيع",
    "الفواتير",
    "المصروفات",
    "العمال",
    "التقارير",
    "الإعدادات"
])

if menu == "نقطة البيع":
    st.switch_page("pages/5_Cashier_POS.py")

elif menu == "الفواتير":
    st.switch_page("pages/5_Cashier_POS.py")

elif menu == "المصروفات":
    st.switch_page("pages/6_Cashier_Expenses.py")

elif menu == "العمال":
    st.switch_page("pages/7_Cashier_Workers.py")

elif menu == "التقارير":
    st.switch_page("pages/8_Cashier_Reports.py")

elif menu == "الإعدادات":
    st.switch_page("pages/9_Cashier_Settings.py")
