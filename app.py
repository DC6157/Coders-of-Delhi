import streamlit as st
import json
import pandas as pd
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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 1.1em;
        opacity: 0.9;
    }
    .user-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .skill-badge {
        display: inline-block;
        background-color: #667eea;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9em;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 2px solid #e0e0e0;
    }
    h1 {
        color: #667eea;
        padding-bottom: 20px;
        text-align: center;
    }
    .highlight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        text-align: center;
    }
    .feature-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        height: 150px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Data Function ---
@st.cache_data
def load_data(filename):
    try:
        if isinstance(filename, str):
            if filename.endswith(".json"):
                with open(filename, "r") as f:
                    data = json.load(f)
            elif filename.endswith(".csv"):
                data = pd.read_csv(filename).to_dict(orient="records")
        else:
            if filename.name.endswith(".json"):
                data = json.load(filename)
            elif filename.name.endswith(".csv"):
                data = pd.read_csv(filename).to_dict(orient="records")
        
        # Handle different data structures
        if isinstance(data, dict):
            # If data is a dict with a list inside
            for key in data.keys():
                if isinstance(data[key], list):
                    return data[key]
            # If data is a single record
            return [data]
        elif isinstance(data, list):
            return data
        else:
            return []
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return []

# --- Clean Data ---
def clean_data(data):
    if not data:
        return []
    
    # If data doesn't have 'name' field, try to use first column as name
    cleaned = []
    for user in data:
        if isinstance(user, dict):
            # Check if 'name' exists, if not use first available field
            if "name" not in user and len(user) > 0:
                first_key = list(user.keys())[0]
                user["name"] = user.get(first_key, "Unknown")
            
            # Only keep records with some data
            if user.get("name", "").strip():
                cleaned.append(user)
    
    return cleaned

# --- Analyze Data ---
def analyze_data(data):
    df = pd.DataFrame(data)
    
    stats = {
        "total_users": len(df),
        "active_users": len(df[df.get("status", "active") == "active"]) if "status" in df.columns else len(df),
        "total_projects": int(df["projects"].sum()) if "projects" in df.columns else 0,
        "avg_experience": round(df["experience"].mean(), 1) if "experience" in df.columns else 0
    }
    
    return df, stats

# --- Create Simple Charts ---
def create_bar_chart(data_dict, title):
    st.markdown(f"**{title}**")
    max_val = max(data_dict.values()) if data_dict else 1
    
    for label, value in sorted(data_dict.items(), key=lambda x: x[1], reverse=True):
        percentage = (value / max_val) * 100
        st.markdown(f"""
            <div style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>{label}</span>
                    <span><b>{value}</b></span>
                </div>
                <div style="background-color: #e0e0e0; border-radius: 5px; height: 25px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                                width: {percentage}%; height: 100%; border-radius: 5px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- Main App ---
st.title("👨‍💻 Coders of Delhi Dashboard")
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #666;'>📊 Comprehensive Analytics & Insights</p>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("# 💻")
    st.markdown("</div>", unsafe_allow_html=True)
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
    
    st.markdown("---")
    st.markdown("### 📚 Features")
    st.markdown("- 👥 User Management")
    st.markdown("- 📊 Data Analytics")
    st.markdown("- 🔍 Advanced Search")
    st.markdown("- 💾 Export Options")

# --- Main Content ---
if uploaded_file is not None:
    # Load and clean data
    data = load_data(uploaded_file)
    data = clean_data(data)
    
    if not data:
        st.error("❌ No valid data found in the uploaded file.")
        
        # Debug information
        with st.expander("🔍 Debug Information - Click to see what went wrong"):
            st.write("**File Name:**", uploaded_file.name)
            st.write("**File Type:**", uploaded_file.type)
            st.write("**File Size:**", uploaded_file.size, "bytes")
            
            # Try to show raw data
            try:
                uploaded_file.seek(0)
                if uploaded_file.name.endswith('.json'):
                    raw_data = json.load(uploaded_file)
                    st.write("**Raw JSON Data:**")
                    st.json(raw_data)
                elif uploaded_file.name.endswith('.csv'):
                    uploaded_file.seek(0)
                    raw_df = pd.read_csv(uploaded_file)
                    st.write("**Raw CSV Data:**")
                    st.dataframe(raw_df.head())
                    st.write("**Columns:**", list(raw_df.columns))
            except Exception as e:
                st.error(f"Could not read file: {str(e)}")
            
            st.info("""
            **Expected Data Format:**
            
            **For JSON:**
            ```json
            [
                {"name": "John", "id": "123", "skills": "Python,JS"},
                {"name": "Jane", "id": "124", "skills": "React,Node"}
            ]
            ```
            
            **For CSV:**
            ```
            name,id,skills
            John,123,"Python,JS"
            Jane,124,"React,Node"
            ```
            """)
        st.stop()
    
    df, stats = analyze_data(data)
    
    # --- Key Metrics Row ---
    st.markdown("## 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">👥 Total Users</div>
                <div class="metric-value">{stats["total_users"]}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        percentage = round(stats['active_users']/stats['total_users']*100) if stats['total_users'] > 0 else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">✅ Active Users</div>
                <div class="metric-value">{stats["active_users"]}</div>
                <div style="font-size: 0.9em;">{percentage}% Active</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💼 Total Projects</div>
                <div class="metric-value">{stats["total_projects"]}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⭐ Avg Experience</div>
                <div class="metric-value">{stats["avg_experience"]}</div>
                <div style="font-size: 0.9em;">Years</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Tabs for Different Views ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👤 User Details", "📈 Analytics", "🔍 Search"])
    
    with tab1:
        st.markdown("### 📋 Data Overview")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("#### User List")
            # Display user table
            display_df = df[["name", "id"]].head(15) if "id" in df.columns else df[["name"]].head(15)
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # Pagination info
            total_users = len(df)
            if total_users > 15:
                st.info(f"Showing 15 of {total_users} users")
        
        with col2:
            st.markdown("#### Quick Statistics")
            
            # Column statistics
            st.markdown(f"""
                <div class="stat-box">
                    <strong>📊 Data Columns:</strong> {len(df.columns)}<br>
                    <strong>📝 Total Records:</strong> {len(df)}<br>
                    <strong>🔢 Numeric Fields:</strong> {len(df.select_dtypes(include=['number']).columns)}
                </div>
            """, unsafe_allow_html=True)
            
            # Skills distribution
            if "skills" in df.columns:
                st.markdown("#### 🎯 Top Skills")
                all_skills = []
                for skills in df["skills"].dropna():
                    if isinstance(skills, list):
                        all_skills.extend(skills)
                    elif isinstance(skills, str):
                        all_skills.extend([s.strip() for s in skills.split(",")])
                
                if all_skills:
                    skill_counts = pd.Series(all_skills).value_counts().head(8)
                    skill_dict = skill_counts.to_dict()
                    create_bar_chart(skill_dict, "")
    
    with tab2:
        st.markdown("### 👤 User Information")
        
        user_names = {user["name"]: user for user in data}
        selected_user = st.selectbox("🔍 Select a user:", [""] + list(user_names.keys()))
        
        if selected_user:
            user_info = user_names[selected_user]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"<h3 style='color: #667eea;'>👤 {selected_user}</h3>", unsafe_allow_html=True)
                
                # Display user info in a card
                info_html = "<div class='user-card'>"
                for key, value in user_info.items():
                    if key != "name":
                        if key == "skills" and isinstance(value, (list, str)):
                            skills_list = value if isinstance(value, list) else value.split(",")
                            info_html += f"<p><strong>🎯 {key.title()}:</strong><br>"
                            for skill in skills_list:
                                info_html += f"<span class='skill-badge'>{skill.strip()}</span>"
                            info_html += "</p>"
                        else:
                            info_html += f"<p><strong>{key.title()}:</strong> {value}</p>"
                info_html += "</div>"
                st.markdown(info_html, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### ⚡ Quick Actions")
                
                if st.button("📧 Send Email", use_container_width=True):
                    st.success("📧 Email feature coming soon!")
                
                if st.button("💬 Send Message", use_container_width=True):
                    st.success("💬 Messaging feature coming soon!")
                
                if st.button("📊 View Full Profile", use_container_width=True):
                    st.success("📊 Full profile view coming soon!")
                
                if st.button("🔗 Share Profile", use_container_width=True):
                    st.success("🔗 Share feature coming soon!")
        else:
            st.info("👆 Please select a user to view details")
    
    with tab3:
        st.markdown("### 📈 Data Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Experience distribution
            if "experience" in df.columns:
                st.markdown("#### 💼 Experience Distribution")
                exp_bins = pd.cut(df["experience"], bins=[0, 2, 5, 10, 20, 100], 
                                 labels=["0-2 yrs", "3-5 yrs", "6-10 yrs", "11-20 yrs", "20+ yrs"])
                exp_counts = exp_bins.value_counts().sort_index()
                create_bar_chart(exp_counts.to_dict(), "")
        
        with col2:
            # Project distribution
            if "projects" in df.columns:
                st.markdown("#### 📦 Projects Distribution")
                proj_stats = {
                    "Min Projects": int(df["projects"].min()),
                    "Max Projects": int(df["projects"].max()),
                    "Median Projects": int(df["projects"].median()),
                    "Total Projects": int(df["projects"].sum())
                }
                
                for label, value in proj_stats.items():
                    st.markdown(f"""
                        <div class="stat-box">
                            <strong>{label}:</strong> {value}
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Additional statistics
        col3, col4 = st.columns(2)
        
        with col3:
            if "status" in df.columns:
                st.markdown("#### 📊 Status Distribution")
                status_counts = df["status"].value_counts().to_dict()
                create_bar_chart(status_counts, "")
        
        with col4:
            # Data quality metrics
            st.markdown("#### ✅ Data Quality")
            missing_data = df.isnull().sum()
            completeness = ((len(df) - missing_data) / len(df) * 100).round(1)
            
            st.markdown("""
                <div class="stat-box">
                    <strong>📋 Data Completeness</strong>
                </div>
            """, unsafe_allow_html=True)
            
            for col_name in df.columns[:5]:
                comp_pct = completeness[col_name]
                st.markdown(f"{col_name}: {comp_pct}%")
                st.progress(comp_pct / 100)
    
    with tab4:
        st.markdown("### 🔍 Advanced Search")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input(
                "Search by name, skill, or any field:",
                placeholder="Type here to search...",
                key="search"
            )
        
        with col2:
            search_field = st.selectbox(
                "Search in:",
                ["All Fields"] + list(df.columns)
            )
        
        if search_term:
            if search_field == "All Fields":
                filtered_data = [
                    user for user in data
                    if any(search_term.lower() in str(value).lower() for value in user.values())
                ]
            else:
                filtered_data = [
                    user for user in data
                    if search_term.lower() in str(user.get(search_field, "")).lower()
                ]
            
            st.markdown(f"#### 🎯 Found {len(filtered_data)} results")
            
            if filtered_data:
                for i, user in enumerate(filtered_data, 1):
                    with st.expander(f"👤 {i}. {user.get('name', 'Unknown')}"):
                        user_html = "<div class='user-card'>"
                        for key, value in user.items():
                            user_html += f"<p><strong>{key.title()}:</strong> {value}</p>"
                        user_html += "</div>"
                        st.markdown(user_html, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No results found for your search!")
        else:
            st.info("👆 Enter a search term to filter users")
    
    # --- Download Section ---
    st.markdown("---")
    st.markdown("### 💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"coders_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"coders_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        # Summary report
        summary = f"""
        📊 CODERS OF DELHI - DATA SUMMARY
        ================================
        
        Total Users: {stats['total_users']}
        Active Users: {stats['active_users']}
        Total Projects: {stats['total_projects']}
        Average Experience: {stats['avg_experience']} years
        
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        st.download_button(
            label="📄 Download Summary",
            data=summary,
            file_name=f"summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    # --- Welcome Screen ---
    st.markdown("""
        <div class="highlight-card">
            <h2>🎉 Welcome to Coders of Delhi Dashboard!</h2>
            <p style="font-size: 1.2em;">Upload your data file to unlock powerful analytics and insights.</p>
            <p>Supported formats: CSV, JSON</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <h3>📊</h3>
                <h4>Analytics</h4>
                <p>View detailed statistics and visualizations</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-box">
                <h3>👥</h3>
                <h4>User Management</h4>
                <p>Search and manage user profiles</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-box">
                <h3>📈</h3>
                <h4>Insights</h4>
                <p>Gain insights from your data</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Use the sidebar to upload your CSV or JSON file to get started!")
    
    # Sample data format
    with st.expander("📝 Sample Data Format"):
        st.code("""
{
  "name": "John Doe",
  "id": "user123",
  "email": "john@example.com",
  "skills": ["Python", "JavaScript", "React"],
  "experience": 5,
  "projects": 12,
  "status": "active"
}
        """, language="json")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "Made with ❤️ for Coders of Delhi | © 2024"
    "</div>",
    unsafe_allow_html=True
)
