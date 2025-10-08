import streamlit as st
import json
import pandas as pd

# --- Load Data Function ---
def load_data(filename):
    if isinstance(filename, str):  # local file path
        if filename.endswith(".json"):
            with open(filename, "r") as f:
                return json.load(f)
        elif filename.endswith(".csv"):
            return pd.read_csv(filename).to_dict(orient="records")
    else:  # file uploader from Streamlit
        if filename.name.endswith(".json"):
            return json.load(filename)
        elif filename.name.endswith(".csv"):
            return pd.read_csv(filename).to_dict(orient="records")

# --- Clean Data ---
def clean_data(data):
    data = [user for user in data if isinstance(user, dict) and user.get("name", "").strip()]
    return data

# --- App Start ---
st.title("👨‍💻 Coders of Delhi Dashboard")

uploaded_file = st.file_uploader("📂 Upload your data file", type=["csv", "json"])
if uploaded_file is not None:
    data = load_data(uploaded_file)
    data = clean_data(data)
    user_names = {user["name"]: user["id"] for user in data}
    st.success("✅ Data loaded successfully!")
else:
    st.warning("Please upload a data file to continue.")
    st.stop()
