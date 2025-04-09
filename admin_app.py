import streamlit as st
import pandas as pd
from utils.data_utils import load_csv
from utils.ui_helpers import get_now, show_header

st.set_page_config(page_title="لوحة تحكم الأدمن - CleanFoam", page_icon="🧼", layout="wide")

if "authenticated" not in st.session_state or not st.session_state.authenticated or st.session_state.role != "admin":
    st.error("غير مصرح لك بالوصول إلى هذه الصفحة.")
    st.stop()

show_header("لوحة تحكم الأدمن")

menu = st.sidebar.radio("القائمة", [
    "الحركة اليومية",
    "التقارير",
    "إدارة الكاشير",
    "سجل النشاطات",
    "الإعدادات"
])

if menu == "الحركة اليومية":
    sales = load_csv("sales.csv")
    today = get_now().strftime("%Y-%m-%d")
    today_sales = sales[sales['date'] == today]

    st.subheader("الحركة اليومية")
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الكاش", f"{today_sales[today_sales['payment_type'] == 'كاش']['amount'].sum():,.2f}")
    col2.metric("إجمالي الشبكة", f"{today_sales[today_sales['payment_type'] == 'شبكة']['amount'].sum():,.2f}")
    col3.metric("عدد العمليات", len(today_sales))

    if st.button("اليوم السابق"):
        st.session_state.selected_date = (pd.to_datetime(today) - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        st.rerun()

elif menu == "التقارير":
    st.switch_page("pages/2_Admin_Reports.py")

elif menu == "إدارة الكاشير":
    st.switch_page("pages/4_Admin_ManageCashiers.py")

elif menu == "سجل النشاطات":
    st.switch_page("pages/3_Admin_ActivityLog.py")

elif menu == "الإعدادات":
    st.subheader("الإعدادات")
    st.text("(سيتم إضافة إعدادات تغيير كلمة المرور وتحديث البيانات لاحقًا)")
