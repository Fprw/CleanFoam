import pandas as pd
import os

DATA_DIR = "data"

def load_csv(file):
    path = os.path.join(DATA_DIR, file)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()

def save_csv(file, df):
    path = os.path.join(DATA_DIR, file)
    df.to_csv(path, index=False)

def append_csv(file, row_dict):
    df = load_csv(file)
    df = pd.concat([df, pd.DataFrame([row_dict])], ignore_index=True)
    save_csv(file, df)

def load_cashiers():
    return load_csv("cashiers.csv")
