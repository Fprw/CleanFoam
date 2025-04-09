import streamlit as st
from utils.auth_utils import check_admin_credentials, check_cashier_credentials

st.set_page_config(page_title="CleanFoam Login", page_icon="🧼")

st.title("تسجيل الدخول إلى نظام CleanFoam")

username = st.text_input("اسم المستخدم")
password = st.text_input("كلمة المرور", type="password")
login_button = st.button("تسجيل الدخول")

if login_button:
    if username == "Admin" and check_admin_credentials(username, password):
        st.session_state.logged_in = True
        st.session_state.user_type = "admin"
        st.rerun()
    elif check_cashier_credentials(username, password):
        st.session_state.logged_in = True
        st.session_state.user_type = "cashier"
        st.session_state.username = username
        st.rerun()
    else:
        st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")

if "logged_in" in st.session_state and st.session_state.logged_in:
    if st.session_state.user_type == "admin":
        st.switch_page("admin_app.py")
    elif st.session_state.user_type == "cashier":
        st.switch_page("cashier_app.py")
