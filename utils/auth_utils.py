import streamlit as st
import pandas as pd
from config.credentials import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.data_utils import load_cashiers

def authenticate_user(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return "admin"

    df = load_cashiers()
    user = df[df["username"] == username]
    if not user.empty and user.iloc[0]["password"] == password:
        return "cashier"

    return None

def login_user():
    st.title("تسجيل الدخول - CleanFoam")
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
            else:
                st.success("تم تسجيل الدخول ككاشير")
                st.switch_page("cashier_app.py")
        else:
            st.error("بيانات الدخول غير صحيحة")
