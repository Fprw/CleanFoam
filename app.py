import streamlit as st
from utils.auth_utils import login_user
from utils.session_utils import show_admin_dashboard, show_cashier_dashboard

st.set_page_config(page_title="CleanFoam", page_icon="🧼", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""

if not st.session_state.authenticated:
    login_user()
else:
    if st.session_state.role == "admin":
        show_admin_dashboard()
    elif st.session_state.role == "cashier":
        show_cashier_dashboard()
    else:
        st.error("الصلاحية غير معروفة.")
