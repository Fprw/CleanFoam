import streamlit as st
import base64

def play_sound(file_path):
    """
    تشغيل ملف صوتي في واجهة Streamlit.
    """
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

if __name__ == "__main__":
    # اختبار تشغيل الصوت (تأكد من وجود ملف alert_sound.mp3 في المسار الصحيح)
    st.title("اختبار تشغيل الصوت")
    if st.button("تشغيل تنبيه"):
        play_sound("../static/alert_sound.mp3")
        st.info("تم تشغيل صوت التنبيه (إذا كان الملف موجودًا).")
