import streamlit as st
import pandas as pd
from utils.data_utils import load_csv, save_csv
from utils.ui_helpers import get_now

st.title("إعدادات الكاشير")

st.subheader("تصفير اليوم")

code = st.text_input("أدخل رمز التصفير", type="password")
if st.button("تأكيد التصفير"):
    if code == "12345":
        today = get_now().strftime("%Y-%m-%d")
        df = load_csv("sales.csv")
        if not df.empty:
            df_today = df[df["date"] == today]
            df_rest = df[df["date"] != today]
            save_csv("sales.csv", df_rest)

            df_today.to_csv(f"data/archive_{today}.csv", index=False)
            st.success("تم تصفير اليوم وتصدير البيانات.")
        else:
            st.info("لا توجد بيانات اليوم لتصفيرها.")
    else:
        st.error("رمز غير صحيح.")

st.subheader("تغيير كلمة المرور")
cashiers = load_csv("cashiers.csv")
old = st.text_input("كلمة المرور الحالية", type="password")
new = st.text_input("كلمة المرور الجديدة", type="password")
if st.button("تحديث"):
    if old and new:
        i = cashiers[cashiers["username"] == st.session_state.username].index
        if not i.empty and cashiers.loc[i[0], "password"] == old:
            cashiers.loc[i[0], "password"] = new
            save_csv("cashiers.csv", cashiers)
            st.success("تم التحديث.")
        else:
            st.error("كلمة المرور الحالية غير صحيحة.")
