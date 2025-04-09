import streamlit as st
import pandas as pd
from utils.auth_utils import authenticate_user
from config.credentials import ADMIN_USERNAME, ADMIN_PASSWORD

st.set_page_config(page_title="CleanFoam - تسجيل الدخول", page_icon="🧼")
st.title("نظام CleanFoam")
st.subheader("تسجيل الدخول")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = ""

username = st.text_input("اسم المستخدم")
password = st.text_input("كلمة المرور", type="password")

if st.button("دخول"):
    role = authenticate_user(username, password)
    if role:
        st.session_state.authenticated = True
        st.session_state.role = role
        st.session_state.username = username
        if role == "admin":
            st.success("تم تسجيل الدخول كأدمن")
            st.switch_page("admin_app.py")
        elif role == "cashier":
            st.success("تم تسجيل الدخول ككاشير")
            st.switch_page("cashier_app.py")
    else:
        st.error("بيانات الدخول غير صحيحة")
