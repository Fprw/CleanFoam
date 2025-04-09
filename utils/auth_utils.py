import streamlit as st
import pandas as pd
from config.credentials import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.data_utils import load_cashiers

def login_user():
    st.title("تسجيل الدخول - CleanFoam")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.role = "admin"
            st.session_state.username = username
            st.experimental_rerun()
        else:
            df = load_cashiers()
            user = df[df['username'] == username]
            if not user.empty and user.iloc[0]['password'] == password:
                st.session_state.authenticated = True
                st.session_state.role = "cashier"
                st.session_state.username = username
                st.session_state.permissions = user.iloc[0].to_dict()
                st.experimental_rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
