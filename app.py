import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Coders of Delhi Dashboard",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    .highlight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Data Function ---
@st.cache_data
def load_data(filename):
    if isinstance(filename, str):
        if filename.endswith(".json"):
            with open(filename, "r") as f:
                return json.load(f)
        elif filename.endswith(".csv"):
            return pd.read_csv(filename).to_dict(orient="records")
    else:
        if filename.name.endswith(".json"):
            return json.load(filename)
        elif filename.name.endswith(".csv"):
            return pd.read_csv(filename).to_dict(orient="records")

# --- Clean Data ---
def clean_data(data):
    data = [user for user in data if isinstance(user, dict) and user.get("name", "").strip()]
    return data

# --- Analyze Data ---
def analyze_data(data):
    df = pd.DataFrame(data)
    
    stats = {
        "total_users": len(df),
        "active_users": len(df[df.get("status", "active") == "active"]) if "status" in df.columns else len(df),
        "total_projects": df["projects"].sum() if "projects" in df.columns else 0,
        "avg_experience": round(df["experience"].mean(), 1) if "experience" in df.columns else 0
    }
    
    return df, stats

# --- Main App ---
st.title("👨‍💻 Coders of Delhi Dashboard")
st.markdown("### 📊 Comprehensive Analytics & Insights")

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/code.png", width=80)
    st.markdown("## 🎯 Controls")
    
    uploaded_file = st.file_uploader(
        "📂 Upload Data File",
        type=["csv", "json"],
        help="Upload your user data in CSV or JSON format"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Quick Info")
    st.info("Upload your data file to see interactive analytics, charts, and user insights.")
    
    if uploaded_file:
        st.success("✅ File uploaded successfully!")

# --- Main Content ---
if uploaded_file is not None:
    # Load and clean data
    data = load_data(uploaded_file)
    data = clean_data(data)
    
    if not data:
        st.error("❌ No valid data found in the uploaded file.")
        st.stop()
    
    df, stats = analyze_data(data)
    
    # --- Key Metrics Row ---
    st.markdown("## 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Users",
            value=stats["total_users"],
            delta="Active"
        )
    
    with col2:
        st.metric(
            label="✅ Active Users",
            value=stats["active_users"],
            delta=f"{round(stats['active_users']/stats['total_users']*100)}%"
        )
    
    with col3:
        st.metric(
            label="💼 Total Projects",
            value=stats["total_projects"],
            delta="Completed"
        )
    
    with col4:
        st.metric(
            label="⭐ Avg Experience",
            value=f"{stats['avg_experience']} yrs",
            delta="Years"
        )
    
    st.markdown("---")
    
    # --- Tabs for Different Views ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👤 User Details", "📈 Analytics", "🔍 Search"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 User List")
            st.dataframe(
                df[["name", "id"]].head(10) if "id" in df.columns else df[["name"]].head(10),
                use_container_width=True,
                height=400
            )
        
        with col2:
            st.markdown("### 📊 Quick Stats")
            
            # Skills distribution
            if "skills" in df.columns:
                all_skills = []
                for skills in df["skills"].dropna():
                    if isinstance(skills, list):
                        all_skills.extend(skills)
                    elif isinstance(skills, str):
                        all_skills.extend([s.strip() for s in skills.split(",")])
                
                if all_skills:
                    skill_counts = pd.Series(all_skills).value_counts().head(10)
                    fig = px.bar(
                        x=skill_counts.values,
                        y=skill_counts.index,
                        orientation='h',
                        title="Top 10 Skills",
                        labels={'x': 'Count', 'y': 'Skill'},
                        color=skill_counts.values,
                        color_continuous_scale='Viridis'
                    )
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 👤 User Information")
        
        user_names = {user["name"]: user for user in data}
        selected_user = st.selectbox("Select a user:", list(user_names.keys()))
        
        if selected_user:
            user_info = user_names[selected_user]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"#### {selected_user}")
                for key, value in user_info.items():
                    if key != "name":
                        st.write(f"**{key.title()}:** {value}")
            
            with col2:
                st.markdown("#### Quick Actions")
                if st.button("📧 Send Email", use_container_width=True):
                    st.info("Email feature coming soon!")
                if st.button("💬 Message", use_container_width=True):
                    st.info("Messaging feature coming soon!")
                if st.button("📊 View Profile", use_container_width=True):
                    st.info("Profile view coming soon!")
    
    with tab3:
        st.markdown("### 📈 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Experience distribution
            if "experience" in df.columns:
                fig = px.histogram(
                    df,
                    x="experience",
                    nbins=20,
                    title="Experience Distribution",
                    labels={'experience': 'Years of Experience', 'count': 'Number of Users'},
                    color_discrete_sequence=['#667eea']
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Project distribution
            if "projects" in df.columns:
                fig = px.box(
                    df,
                    y="projects",
                    title="Projects Distribution",
                    labels={'projects': 'Number of Projects'},
                    color_discrete_sequence=['#764ba2']
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        if "experience" in df.columns and "projects" in df.columns:
            st.markdown("### 🔥 Correlation Analysis")
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 1:
                corr = df[numeric_cols].corr()
                fig = px.imshow(
                    corr,
                    text_auto=True,
                    aspect="auto",
                    title="Correlation Heatmap",
                    color_continuous_scale='RdBu'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 🔍 Advanced Search")
        
        search_term = st.text_input("Search by name, skill, or any field:", placeholder="Type here...")
        
        if search_term:
            filtered_data = [
                user for user in data
                if any(search_term.lower() in str(value).lower() for value in user.values())
            ]
            
            st.markdown(f"#### Found {len(filtered_data)} results")
            
            if filtered_data:
                for user in filtered_data:
                    with st.expander(f"👤 {user.get('name', 'Unknown')}"):
                        for key, value in user.items():
                            st.write(f"**{key.title()}:** {value}")
            else:
                st.warning("No results found!")
        else:
            st.info("👆 Enter a search term to filter users")
    
    # --- Download Section ---
    st.markdown("---")
    st.markdown("### 💾 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"coders_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name=f"coders_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )

else:
    # --- Welcome Screen ---
    st.markdown("""
        <div class="highlight-card">
            <h2>🎉 Welcome to Coders of Delhi Dashboard!</h2>
            <p>Upload your data file to get started with comprehensive analytics and insights.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Analytics")
        st.write("View detailed statistics and visualizations")
    
    with col2:
        st.markdown("### 👥 User Management")
        st.write("Search and manage user profiles")
    
    with col3:
        st.markdown("### 📈 Insights")
        st.write("Gain insights from your data")
    
    st.info("👈 Use the sidebar to upload your CSV or JSON file")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Made with ❤️ for Coders of Delhi | © 2024</div>",
    unsafe_allow_html=True
)
