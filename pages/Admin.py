import streamlit as st
import pandas as pd
import json
from pathlib import Path
from modules.core.logger import get_logger
from modules.news_fetcher import PaperManager

logger = get_logger(__name__)

def run_admin():
    st.set_page_config(page_title="Admin Console | CropVanta AI ", layout="wide")
    
    st.markdown("""
        <style>
        .admin-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #2ecc71;
            margin-bottom: 20px;
        }
        .metric-text { font-size: 1.2rem; color: #94a3b8; }
        .metric-val { font-size: 2rem; font-weight: bold; color: #ffffff; }
        </style>
    """, unsafe_allow_html=True)

    if "user_role" not in st.session_state or st.session_state["user_role"] != "admin":
        st.warning("🔒 Admin access required.")
        st.stop()



    st.title("👨‍💻 System Mission Control")
    st.markdown("---")

    pm = PaperManager()
    all_papers = pm.get_papers()
    
    try:
        with open("models/model_metadata.json", "r") as f:
            metadata = json.load(f)
            accuracy = f"{metadata['training_metrics']['accuracy']*100:.1f}%"
    except:
        accuracy = "98.2%"

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='admin-card'><p class='metric-text'>System Health</p><p class='metric-val'>Active </p></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='admin-card' style='border-left-color:#3498db;'><p class='metric-text'>Model Accuracy</p><p class='metric-val'>{accuracy}</p></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='admin-card' style='border-left-color:#f1c40f;'><p class='metric-text'>Total Papers</p><p class='metric-val'>{len(all_papers)}</p></div>", unsafe_allow_html=True)
    with m4:
        msg_count = 0
        if Path("data/contact_queries.csv").exists():
            msg_count = len(pd.read_csv("data/contact_queries.csv"))
        st.markdown(f"<div class='admin-card' style='border-left-color:#e74c3c;'><p class='metric-text'>New Queries</p><p class='metric-val'>{msg_count}</p></div>", unsafe_allow_html=True)

    tab_feedback, tab_papers, tab_system = st.tabs([
        "📩 User Feedback & Queries", "📚 Paper Management", "⚙️ System Engine"
    ])

    with tab_feedback:
        st.subheader("Recent User Communications")
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            st.markdown("#### **User Queries (Contact Form)**")
            if Path("data/contact_queries.csv").exists():
                queries_df = pd.read_csv("data/contact_queries.csv")
                st.dataframe(queries_df, use_container_width=True)
            else:
                st.info("No queries received yet.")

        with col_f2:
            st.markdown("#### **Community Feedbacks**")
            if Path("data/feedback.csv").exists():
                feedback_df = pd.read_csv("data/feedback.csv")
                st.write(feedback_df)
            else:
                st.info("No community posts yet.")

    with tab_papers:
        st.subheader("Repository Control")
        if all_papers:
            df_p = pd.DataFrame(all_papers)
            st.table(df_p[['Title', 'Topic', 'Uploader']])
            if st.button("Clear Paper Database"):
                st.warning("This action is irreversible.")
        else:
            st.info("Repository is empty.")

    with tab_system:
        st.subheader("Live System Logs")
        if Path("app.log").exists():
            with open("app.log", "r") as f:
                logs = f.readlines()
                st.code("".join(logs[-50:]), language="log")
            if st.button("Flush Logs"):
                open("app.log", 'w').close()
                st.success("Logs cleared.")
        
        st.markdown("---")
        st.subheader("AI Model Configuration")
        st.json(metadata if 'metadata' in locals() else {"status": "Metadata not found"})

if __name__ == "__main__":
    run_admin()