import streamlit as st
import json

# -------------------------------
# Utility Functions
# -------------------------------
def load_data(filename):
    """Load JSON data from file"""
    with open(filename, "r") as file:
        return json.load(file)

def clean_data(data):
    """Clean users and pages"""
    data["users"] = [user for user in data["users"] if user["name"].strip()]
    for user in data["users"]:
        user["friends"] = list(set(user["friends"]))
    data["users"] = [user for user in data["users"] if user["friends"] or user["liked_pages"]]

    unique_pages = {}
    for page in data["pages"]:
        unique_pages[page["id"]] = page
    data["pages"] = list(unique_pages.values())

    return data

def find_people_you_may_know(user_id, data):
    """Recommend friends based on mutual connections"""
    user_friends = {u["id"]: set(u["friends"]) for u in data["users"]}
    if user_id not in user_friends:
        return []

    direct_friends = user_friends[user_id]
    suggestions = {}
    for friend in direct_friends:
        for mutual in user_friends.get(friend, []):
            if mutual != user_id and mutual not in direct_friends:
                suggestions[mutual] = suggestions.get(mutual, 0) + 1

    sorted_suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
    return [uid for uid, _ in sorted_suggestions]

def find_pages_you_might_like(user_id, data):
    """Recommend pages based on shared interests"""
    user_pages = {u["id"]: set(u["liked_pages"]) for u in data["users"]}
    if user_id not in user_pages:
        return []

    liked_pages = user_pages[user_id]
    suggestions = {}
    for other_user, pages in user_pages.items():
        if other_user != user_id:
            shared = liked_pages.intersection(pages)
            for page in pages:
                if page not in liked_pages:
                    suggestions[page] = suggestions.get(page, 0) + len(shared)

    sorted_pages = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
    return [pid for pid, _ in sorted_pages]

# -------------------------------
# Streamlit App UI
# -------------------------------
st.set_page_config(page_title="Coders of Delhi", page_icon="💻", layout="wide")

st.title("💻 Coders of Delhi")
st.subheader("A Pure Python Social Network Simulation")

# Upload JSON data
uploaded_file = st.file_uploader("📂 Upload your data file (e.g., massive_data.json)", type=["json"])

if uploaded_file:
    data = json.load(uploaded_file)
    data = clean_data(data)

    # Select User
    user_names = {user["name"]: user["id"] for user in data["users"]}
    user_choice = st.selectbox("👤 Choose a User", list(user_names.keys()))
    user_id = user_names[user_choice]

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤝 People You May Know")
        friend_recs = find_people_you_may_know(user_id, data)
        if friend_recs:
            for fid in friend_recs:
                friend = next((u for u in data["users"] if u["id"] == fid), None)
                if friend:
                    st.write(f"👤 **{friend['name']}** (ID: {fid})")
        else:
            st.info("No friend recommendations found.")

    with col2:
        st.subheader("📄 Pages You Might Like")
        page_recs = find_pages_you_might_like(user_id, data)
        if page_recs:
            for pid in page_recs:
                page = next((p for p in data["pages"] if p["id"] == pid), None)
                if page:
                    st.write(f"📘 **{page['name']}** (Page ID: {pid})")
        else:
            st.info("No page recommendations found.")

    st.markdown("---")
    st.success("✅ Analysis complete! Explore recommendations above.")

else:
    st.info("Please upload a valid JSON dataset to get started.")
