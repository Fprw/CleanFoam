import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

def get_now():
    return datetime.now(ZoneInfo("Asia/Riyadh"))

def show_header(title=""):
    now = get_now()
    st.title(title)
    st.write(f"التاريخ والوقت الحالي: {now.strftime('%Y-%m-%d %H:%M:%S')}")
