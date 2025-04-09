import os
import pandas as pd

DATA_DIR = "data"
SALES_FILE = os.path.join(DATA_DIR, "sales.csv")
WORKERS_FILE = os.path.join(DATA_DIR, "workers.csv")

def save_sales_data(new_sales_df):
    """
    حفظ بيانات مبيعات جديدة إلى ملف CSV.
    إذا كان الملف موجودًا، يتم إلحاق البيانات الجديدة به.
    إذا لم يكن موجودًا، يتم إنشاء ملف جديد مع البيانات الجديدة.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if os.path.exists(SALES_FILE):
        try:
            existing_sales_df = pd.read_csv(SALES_FILE)
            updated_sales_df = pd.concat([existing_sales_df, new_sales_df], ignore_index=True)
            updated_sales_df.to_csv(SALES_FILE, index=False)
        except FileNotFoundError:
            new_sales_df.to_csv(SALES_FILE, index=False)
    else:
        new_sales_df.to_csv(SALES_FILE, index=False)

def load_workers_data():
    """
    تحميل بيانات العمال من ملف CSV.
    إذا لم يكن الملف موجودًا، يتم إنشاء ملف فارغ.
    """
    if not os.path.exists(WORKERS_FILE):
        return pd.DataFrame(columns=["name"])
    try:
        return pd.read_csv(WORKERS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["name"])

if __name__ == "__main__":
    # اختبار حفظ بيانات المبيعات
    example_sale1 = pd.DataFrame({
        "worker_name": ["علي"],
        "amount": [25.0],
        "payment_method": ["كاش"],
        "date": ["2025-04-09"],
        "time": ["18:00:00"],
        "cashier": ["كاشير1"]
    })
    save_sales_data(example_sale1)
    print(f"تم حفظ بيانات البيع الأولى في {SALES_FILE}")

    example_sale2 = pd.DataFrame({
        "worker_name": ["محمد"],
        "amount": [30.0],
        "payment_method": ["شبكة"],
        "date": ["2025-04-09"],
        "time": ["18:15:00"],
        "cashier": ["كاشير1"]
    })
    save_sales_data(example_sale2)
    print(f"تم حفظ بيانات البيع الثانية في {SALES_FILE}")

    # اختبار تحميل بيانات العمال (سيكون فارغًا في البداية)
    workers = load_workers_data()
    print("\nبيانات العمال:")
    print(workers)

    # يمكنك إضافة ملف workers.csv يدويًا في مجلد data/ لاختبار التحميل
    # مثال لمحتوى workers.csv:
    # name
    # أحمد
    # خالد
    # سالم
