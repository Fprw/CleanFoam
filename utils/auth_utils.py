import os
import pandas as pd
from config.credentials import ADMIN_USERNAME, ADMIN_PASSWORD

DATA_DIR = "data"
CASHIERS_FILE = os.path.join(DATA_DIR, "cashiers.csv")

def check_admin_credentials(username, password):
    """
    التحقق من بيانات اعتماد المسؤول.
    """
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def load_cashiers():
    """
    تحميل بيانات الكاشيرين من ملف CSV.
    إذا لم يكن الملف موجودًا، يتم إنشاء ملف فارغ.
    """
    if not os.path.exists(CASHIERS_FILE):
        return pd.DataFrame(columns=["username", "password", "permissions"])
    try:
        return pd.read_csv(CASHIERS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["username", "password", "permissions"])

def check_cashier_credentials(username, password):
    """
    التحقق من بيانات اعتماد الكاشير.
    """
    cashiers_df = load_cashiers()
    cashier = cashiers_df[cashiers_df["username"] == username]
    if not cashier.empty:
        return cashier["password"].iloc[0] == password
    return False

if __name__ == "__main__":
    # اختبار الدوال بشكل مبدئي
    print(f"هل بيانات الأدمن صحيحة؟: {check_admin_credentials('Admin', 'CF3010@@')}")
    print(f"هل بيانات الأدمن خاطئة؟: {check_admin_credentials('Admin', 'wrong_password')}")

    # مثال على تحميل الكاشيرين (سيظهر فارغًا في البداية)
    cashiers = load_cashiers()
    print("\nبيانات الكاشيرين:")
    print(cashiers)

    # يمكنك إضافة المزيد من الاختبارات هنا بعد إضافة بيانات إلى cashiers.csv
