import streamlit as st
import pandas as pd
import os
from utils.auth_utils import load_cashiers
from config.credentials import ADMIN_USERNAME  # Import for display purposes
import datetime
import pytz

DATA_DIR = "data"
SALES_FILE = os.path.join(DATA_DIR, "sales.csv")

# Set the timezone for Saudi Arabia (Jeddah)
jeddah_tz = pytz.timezone('Asia/Riyadh')

def get_current_date():
    """Returns the current date in Jeddah timezone."""
    return datetime.datetime.now(jeddah_tz).date()

def load_sales_data(date=None):
    """Loads sales data from CSV. If date is provided, filter for that date."""
    if not os.path.exists(SALES_FILE):
        return pd.DataFrame(columns=["worker_name", "amount", "payment_method", "date", "time", "cashier"])
    try:
        df = pd.read_csv(SALES_FILE)
        if date:
            df['date'] = pd.to_datetime(df['date']).dt.date
            return df[df['date'] == date]
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["worker_name", "amount", "payment_method", "date", "time", "cashier"])

def display_daily_stats(sales_df):
    """Displays daily statistics (cash, network, total bills)."""
    if sales_df.empty:
        st.info("لا توجد مبيعات مسجلة لهذا اليوم.")
        return

    cash_sales = sales_df[sales_df['payment_method'] == 'كاش']['amount'].sum()
    network_sales = sales_df[sales_df['payment_method'] == 'شبكة']['amount'].sum()
    total_bills = len(sales_df)

    st.subheader("إحصائيات الحركة اليومية")
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الكاش", f"{cash_sales:.2f} ريال")
    col2.metric("إجمالي الشبكة", f"{network_sales:.2f} ريال")
    col3.metric("عدد الفواتير", total_bills)

def admin_page():
    st.title(f"لوحة تحكم الأدمن ({ADMIN_USERNAME})")

    today = get_current_date()
    yesterday = today - datetime.timedelta(days=1)
    two_days_ago = today - datetime.timedelta(days=2)

    selected_date = st.sidebar.radio("تصفح الأيام", [f"اليوم ({today.strftime('%Y-%m-%d')})",
                                                    f"أمس ({yesterday.strftime('%Y-%m-%d')})",
                                                    f"قبل أمس ({two_days_ago.strftime('%Y-%m-%d')})"])

    if "اليوم" in selected_date:
        current_sales = load_sales_data(today)
        display_daily_stats(current_sales)
    elif "أمس" in selected_date:
        yesterday_sales = load_sales_data(yesterday)
        display_daily_stats(yesterday_sales)
    elif "قبل أمس" in selected_date:
        two_days_ago_sales = load_sales_data(two_days_ago)
        display_daily_stats(two_days_ago_sales)

    st.sidebar.title("القائمة")
    menu = st.sidebar.radio("اختر صفحة", ["الحركة اليومية", "التقارير", "إدارة الكاشير", "سجل النشاطات", "الإعدادات"])

    if menu == "الحركة اليومية":
        st.subheader("الحركة اليومية")
        # سيتم إضافة تفاصيل الحركة اليومية هنا
    elif menu == "التقارير":
        st.subheader("التقارير")
        # سيتم إضافة خيارات التقارير هنا
    elif menu == "إدارة الكاشير":
        st.subheader("إدارة الكاشير")
        cashiers_df = load_cashiers()
        st.write("الكاشيرون المسجلون:")
        st.dataframe(cashiers_df)
        # سيتم إضافة خيارات إنشاء، تعديل، وحذف الكاشير هنا
    elif menu == "سجل النشاطات":
        st.subheader("سجل النشاطات")
        # سيتم عرض سجل النشاطات هنا
    elif menu == "الإعدادات":
        st.subheader("الإعدادات")
        # سيتم إضافة خيارات الإعدادات هنا

if __name__ == "__main__":
    if "logged_in" in st.session_state and st.session_state.logged_in and st.session_state.user_type == "admin":
        admin_page()
    else:
        st.warning("يرجى تسجيل الدخول كمسؤول.")
