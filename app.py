import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ------------------------------------------------------
# 🧠 App Configuration
# ------------------------------------------------------
st.set_page_config(
    page_title="Coder of Delhi | ML Predictor",
    page_icon="🤖",
    layout="wide"
)

# ------------------------------------------------------
# 🏷️ App Title and Description
# ------------------------------------------------------
st.title("🚀 Coder of Delhi – Machine Learning Web App")
st.markdown("""
Welcome to **Coder of Delhi**, an interactive machine learning platform.  
Upload your dataset, train a model, and make predictions — all in one place!
""")

# ------------------------------------------------------
# 📂 Data Upload Section
# ------------------------------------------------------
st.header("1️⃣ Upload Dataset")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    # ------------------------------------------------------
    # ⚙️ Model Training Section
    # ------------------------------------------------------
    st.header("2️⃣ Train Your Model")
    all_columns = df.columns.tolist()
    target = st.selectbox("🎯 Select Target Column", all_columns)
    features = st.multiselect("🧩 Select Feature Columns", [col for col in all_columns if col != tar_]()
