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
    features = st.multiselect("🧩 Select Feature Columns", [col for col in all_columns if col != target])

    if st.button("Train Model"):
        if not features:
            st.warning("⚠️ Please select at least one feature column before training.")
        else:
            X = df[features]
            y = df[target]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)

            st.success(f"✅ Model Trained Successfully! Accuracy: **{accuracy:.2f}**")

            # ------------------------------------------------------
            # 🔮 Prediction Section
            # ------------------------------------------------------
            st.header("3️⃣ Make Predictions")
            st.write("Enter feature values below to make a prediction:")

            input_data = {}
            for feature in features:
                value = st.number_input(
                    f"Enter value for {feature}",
                    float(df[feature].min()),
                    float(df[feature].max()),
                    float(df[feature].mean())
                )
                input_data[feature] = value

            if st.button("Predict"):
                input_df = pd.DataFrame([input_data])
                prediction = model.predict(input_df)[0]
                st.success(f"🎯 Predicted Result: **{prediction}**")

else:
    st.info("👆 Upload a dataset above to get started!")

# ------------------------------------------------------
# 🧾 Footer
# ------------------------------------------------------
st.markdown("---")
st.caption("🧠 Project by **Coder of Delhi** | Built with ❤️ using Streamlit")

