import streamlit as st
import pandas as pd
import os
import datetime
import pytz
from utils.auth_utils import load_cashiers
from utils.data_utils import save_sales_data, load_workers_data
from utils.ui_helpers import play_sound

DATA_DIR = "data"
SALES_FILE = os.path.join(DATA_DIR, "sales.csv")
WORKERS_FILE = os.path.join(DATA_DIR, "workers.csv")
ALERT_SOUND_PATH = "static/alert_sound.mp3"

# Set the timezone for Saudi Arabia (Jeddah)
jeddah_tz = pytz.timezone('Asia/Riyadh')

def get_current_datetime():
    """Returns the current datetime in Jeddah timezone."""
    return datetime.datetime.now(jeddah_tz)

def cashier_page():
    st.title(f"واجهة الكاشير ({st.session_state.username})")

    # نقطة البيع
    with st.container():
        st.subheader("نقطة البيع")
        workers_df = load_workers_data()
        worker_names = ["اختر العامل"] + workers_df['name'].tolist() if not workers_df.empty else ["لا يوجد عمال مسجلين"]
        selected_worker = st.selectbox("اسم العامل", worker_names)
        amount = st.number_input("المبلغ", min_value=0.01)
        payment_method = st.radio("نوع الدفع", ["كاش", "شبكة"])
        sell_button = st.button("بيع")

        if sell_button:
            if selected_worker == "اختر العامل" or selected_worker == "لا يوجد عمال مسجلين":
                st.error("يرجى اختيار اسم العامل.")
            elif amount <= 0:
                st.error("يرجى إدخال مبلغ صحيح.")
            else:
                current_datetime = get_current_datetime()
                new_sale = pd.DataFrame({
                    "worker_name": [selected_worker],
                    "amount": [amount],
                    "payment_method": [payment_method],
                    "date": [current_datetime.date()],
                    "time": [current_datetime.strftime("%H:%M:%S")],
                    "cashier": [st.session_state.username]
                })
                save_sales_data(new_sale)
                st.success("تم تسجيل الفاتورة بنجاح!")
                play_sound(ALERT_SOUND_PATH)
                # Reset fields (optional, Streamlit will rerun and reset anyway)

    st.sidebar.title("القائمة")
    menu = st.sidebar.radio("اختر صفحة", ["نقطة البيع", "الفواتير", "المصروفات", "العمال", "التقارير", "الإعدادات"])

    if menu == "نقطة البيع":
        pass # نقطة البيع معروضة بالفعل أعلاه
    elif menu == "الفواتير":
        st.subheader("الفواتير")
        # سيتم إضافة خيارات تعديل وحذف الفواتير هنا
    elif menu == "المصروفات":
        st.subheader("المصروفات")
        # سيتم إضافة خيارات المصروفات العامة ومصروفات العمال هنا
    elif menu == "العمال":
        st.subheader("العمال")
        # سيتم إضافة خيارات إضافة وحذف العمال هنا
    elif menu == "التقارير":
        st.subheader("التقارير")
        # سيتم إضافة خيارات التقارير الخاصة بالكاشير هنا
    elif menu == "الإعدادات":
        st.subheader("الإعدادات")
        # سيتم إضافة خيارات تصفير البيانات وتغيير كلمة المرور هنا

if __name__ == "__main__":
    if "logged_in" in st.session_state and st.session_state.logged_in and st.session_state.user_type == "cashier":
        cashier_page()
    else:
        st.warning("يرجى تسجيل الدخول ككاشير.")
