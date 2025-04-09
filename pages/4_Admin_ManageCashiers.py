import streamlit as st
import pandas as pd
from utils.data_utils import load_csv, save_csv

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("يرجى تسجيل الدخول أولاً.")
    st.stop()

if st.session_state.role != "admin":
    st.error("غير مصرح لك بالدخول إلى هذه الصفحة.")
    st.stop()

st.title("إدارة الكاشيرين")

cashiers = load_csv("cashiers.csv")

st.subheader("إضافة كاشير جديد")

with st.form("add_cashier"):
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور")
    
    col1, col2, col3 = st.columns(3)
    can_sell = col1.checkbox("صلاحية البيع")
    can_expense = col2.checkbox("صلاحية المصروفات")
    can_reset = col3.checkbox("صلاحية التصفير")

    col4, col5 = st.columns(2)
    can_manage_workers = col4.checkbox("إدارة العمال")
    can_send_report = col5.checkbox("إرسال تقرير يومي")

    submitted = st.form_submit_button("إضافة")

    if submitted and username and password:
        if username in cashiers["username"].values:
            st.warning("اسم المستخدم موجود مسبقاً.")
        else:
            new_row = pd.DataFrame([{
                "username": username,
                "password": password,
                "can_sell": can_sell,
                "can_expense": can_expense,
                "can_reset": can_reset,
                "can_manage_workers": can_manage_workers,
                "can_send_report": can_send_report
            }])
            updated = pd.concat([cashiers, new_row], ignore_index=True)
            save_csv("cashiers.csv", updated)
            st.success("تمت الإضافة بنجاح.")
            st.experimental_rerun()

st.markdown("---")
st.subheader("الكاشيرون الحاليون")

if not cashiers.empty:
    st.dataframe(cashiers.drop(columns=["password"]), use_container_width=True)

    to_delete = st.selectbox("اختر كاشير لحذفه", [""] + cashiers["username"].tolist())
    if st.button("حذف الكاشير"):
        if to_delete:
            cashiers = cashiers[cashiers["username"] != to_delete]
            save_csv("cashiers.csv", cashiers)
            st.success("تم حذف الكاشير.")
            st.experimental_rerun()
