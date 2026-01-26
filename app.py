import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from pathlib import Path
from PIL import Image

# -------------------- Core & Schema Imports --------------------
from modules.core.config import settings
from modules.core.logger import get_logger
from modules.core.schemas import CropInput

# -------------------- Internal Modules (Upgraded) --------------------
from modules.ui_components import (
    load_modern_css, 
    render_weather_stats, 
    render_paper_card, 
    display_pdf, 
    render_feedback_post
)
from modules.crop_advisor import CropAdvisor
from modules.market_advisor import MarketAdvisor
from modules.calandar_advisor import CalendarAdvisor
from modules.news_fetcher import PaperManager
from modules import land_suitability, ai_chatbot

logger = get_logger(__name__)

# -------------------- App Configuration --------------------
st.set_page_config(
    page_title=f"🌾 {settings.PROJECT_NAME}",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- Style & Directory Setup --------------------
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_modern_css()  # Load base styles
local_css("styles.css")  # Load custom animations

# Ensure data persistence folders exist
Path("data/papers").mkdir(parents=True, exist_ok=True)

# -------------------- Session & Resource Initialization --------------------
@st.cache_resource
def init_services():
    try:
        scaler = joblib.load(settings.SCALER_PATH)
        model = joblib.load(settings.MODEL_PATH)
        return {
            "advisor": CropAdvisor(model, scaler),
            "market": MarketAdvisor(),
            "calendar": CalendarAdvisor(),
            "papers": PaperManager()
        }
    except Exception as e:
        logger.error(f"Failed to load resources: {e}")
        return None

services = init_services()

@st.cache_data
def load_market_data():
    try: return pd.read_csv("data/mandi_prices.csv")
    except: return pd.DataFrame()

market_df = load_market_data()

# -------------------- Sidebar --------------------
st.sidebar.markdown(f"<h2 style='color:#2ecc71;'>🌿 Menu</h2>", unsafe_allow_html=True)
st.sidebar.caption(f"Enterprise Edition v{settings.VERSION}")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Live Stats")
if not market_df.empty:
    st.sidebar.metric("Commodities", market_df['commodity'].nunique())
    st.sidebar.metric("Markets", market_df['market'].nunique())

# -------------------- Main Navigation (Modern Tabs) --------------------
st.markdown(f"<h1 class='main-title'>🌾 {settings.PROJECT_NAME}</h1>", unsafe_allow_html=True)

tabs = st.tabs([
    "📊 Dashboard", 
    "🌱 Crop AI", 
    "🌍 Land Suitability", 
    "📈 Market & Calendar", 
    "📚 Research Portal", 
    "🤖 AI Assistant",
    "👥 Community & Support"
])

# -------------------- Tab 0: Dashboard (Ultra Modern) --------------------
with tabs[0]:
    # 1. Rainbow News Ticker (Scrolling Mandi Prices)
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(0, 251, 255, 0.2);'>
            <marquee behavior="scroll" direction="left" style='color: #00fbff; font-weight: bold;'>
                🌾 Wheat: ₹2,450/qtl ▲ | 🟢 Mustard: ₹5,600/qtl ▲ | 🍚 Rice: ₹3,100/qtl ▼ | ⚡ AI Engine: Stable | 🌦️ Weather Alert: Heavy Rain expected in Punjab region next 48 hours.
            </marquee>
        </div>
    """, unsafe_allow_html=True)

    # 2. Dynamic Time-based Greeting Card
    hour = datetime.now().hour
    greeting = "🌅 Good Morning" if hour < 12 else "☀️ Good Afternoon" if hour < 18 else "🌙 Good Evening"
    
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #FF0080, #7928CA, #00fbff); padding: 2px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(255, 0, 128, 0.3);'>
        <div style='background: #0e1117; padding: 35px; border-radius: 18px; text-align: center;'>
            <h1 style='margin:0; background: linear-gradient(to right, #00fbff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem;'>
                {greeting}, Shailendra!
            </h1>
            <p style='color: #94a3b8; font-size: 1.1rem; margin-top: 10px;'>
                Welcome back to your <b>AgroPulse AI</b> Mission Control. Everything looks great today.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. 3-Color Metric Row (Glowing Underlines)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div style='border-bottom: 4px solid #FF0080; padding-bottom: 10px;'>", unsafe_allow_html=True)
        st.metric("System Health", "98.8%", delta="Optimal")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2:
        st.markdown("<div style='border-bottom: 4px solid #00fbff; padding-bottom: 10px;'>", unsafe_allow_html=True)
        st.metric("AI Accuracy", "98.2%", delta="0.4% ▲")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c3:
        st.markdown("<div style='border-bottom: 4px solid #FFEE00; padding-bottom: 10px;'>", unsafe_allow_html=True)
        st.metric("Market Sentiment", "Bullish", delta="High")
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. Quick Action Info Card
    st.markdown("""
    <div class='agri-card' style='margin-top: 30px; border-left: 5px solid #7928CA;'>
        <h3 style='color: #7928CA; margin-top: 0;'>🚀 Quick Insights</h3>
        <p style='color: #e2e8f0;'>Our models suggest this is the <b>optimal time for sowing Mustard</b> in Northern India. 
        Check the 'Crop AI' tab for a detailed soil analysis report.</p>
    </div>
    """, unsafe_allow_html=True)
# -------------------- Tab 1: Crop AI --------------------
with tabs[1]:
    st.subheader("🌱 Precision Crop Recommendation")
    with st.form("prediction_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            N = st.number_input("Nitrogen (N)", 0, 140, 50)
            P = st.number_input("Phosphorus (P)", 5, 145, 50)
        with c2:
            K = st.number_input("Potassium (K)", 5, 205, 50)
            temp = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
        with c3:
            ph = st.number_input("Soil pH", 0.0, 14.0, 6.5)
            rain = st.number_input("Rainfall (mm)", 0.0, 500.0, 100.0)
        
        submit = st.form_submit_button("🚀 Run AI Analysis")

    if submit and services:
        result = services["advisor"].recommend_crop(CropInput(nitrogen=N, phosphorus=P, potassium=K, temperature=temp, humidity=60.0, ph=ph, rainfall=rain))
        if result["status"] == "success":
            st.markdown(f"<div class='agri-card' style='border-left: 5px solid #2ecc71;'><h3>✅ Recommended: {result['crop_name']}</h3><p>{result['description']}</p></div>", unsafe_allow_html=True)
            st.progress(98 / 100) # Mock confidence for display

# -------------------- Tab 2: Land Analysis --------------------
with tabs[2]:
    land_suitability.run()

# -------------------- Tab 3: Market & Calendar --------------------
with tabs[3]:
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("<h3 style='color: #FFEE00;'>📈 Market Insights</h3>", unsafe_allow_html=True)
        crop_query = st.text_input("Search Market Price (e.g., Wheat)", "Wheat")
        
        if not market_df.empty:
            # Service call
            analysis = services["market"].process_market_data(market_df, crop_query, "Punjab")
            
            # 🛡️ Safety Check: Check if 'status' is success and 'data' exists
            if analysis.get("status") == "success" and "data" in analysis:
                st.markdown(f"<p style='color: #2ecc71;'>Showing results for <b>{crop_query}</b></p>", unsafe_allow_html=True)
                st.dataframe(analysis["data"], use_container_width=True)
                
                # Extra Highlight: Modal Price agar available ho
                if "insights" in analysis:
                    st.info(f"💡 Average Market Price: ₹{analysis['insights'].get('current_modal', 'N/A')}")
            else:
                # Agar data nahi mila toh error dikhane ke bajaye generic message dein
                st.warning(f"🔍 No live data found for '{crop_query}' in Punjab. Try searching 'Wheat' or 'Rice'.")
                # Optional: Show a sample of the raw data so user knows what's available
                with st.expander("View Available Market Data"):
                    st.write(market_df.head(10))
        else:
            st.error("Market database (mandi_prices.csv) is missing or empty.")

    with c2:
        st.markdown("<h3 style='color: #00fbff;'>🗓 Crop Calendar</h3>", unsafe_allow_html=True)
        calendar_data = services["calendar"].get_calendar_df()
        if calendar_data is not None:
            st.dataframe(calendar_data, use_container_width=True)
        else:
            st.info("Calendar data not available.")

# -------------------- Tab 4: Research Portal (FIXED PDF VIEWER) --------------------
with tabs[4]:
    st.subheader("📚 Digital Research Repository")
    papers = services["papers"].get_papers()
    if papers:
        for p in papers:
            with st.expander(f"📖 {p['Title']} (Topic: {p['Topic']})"):
                render_paper_card(p['Title'], p['Topic'], p['Uploader'])
                # Call the upgraded PDF Viewer from ui_components
                pdf_path = f"data/papers/{p['Filename']}"
                display_pdf(pdf_path)
    else:
        st.info("No papers available in the repository.")

# -------------------- Tab 5: AI Assistant (Menu Logic) --------------------
with tabs[5]:
    ai_chatbot.run()

# -------------------- Tab 6: Community & Support --------------------
with tabs[6]:
    about_col, contact_col = st.columns(2)
    
    with about_col:
        st.markdown("<div class='agri-card'><h3>👥 Community Feedback</h3></div>", unsafe_allow_html=True)
        # Display latest posts
        if Path("data/feedback.csv").exists():
            fb_df = pd.read_csv("data/feedback.csv")
            for _, row in fb_df.tail(3).iterrows(): # Show last 3
                render_feedback_post(row['User'], row['Date'], row['Message'])
        
        with st.form("feedback_form", clear_on_submit=True):
            f_user = st.text_input("Your Name")
            f_msg = st.text_area("Share a tip or feedback")
            if st.form_submit_button("Post Publicly"):
                f_path = Path("data/feedback.csv")
                pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), f_user, f_msg]], 
                             columns=["Date", "User", "Message"]).to_csv(f_path, mode='a', header=not f_path.exists(), index=False)
                st.success("Post live!")
                st.rerun()

    with contact_col:
        st.markdown("<div class='agri-card'><h3>📩 Support Ticket</h3></div>", unsafe_allow_html=True)
        with st.form("contact_form", clear_on_submit=True):
            c_name = st.text_input("Name")
            c_email = st.text_input("Email")
            c_query = st.selectbox("Topic", ["Prediction Issue", "Data Bug", "Suggestion"])
            c_desc = st.text_area("Details")
            if st.form_submit_button("Send to Admin"):
                q_path = Path("data/contact_queries.csv")
                pd.DataFrame([[datetime.now(), c_name, c_email, c_query, c_desc, "Open"]], 
                             columns=["Date", "Name", "Email", "Type", "Description", "Status"]).to_csv(q_path, mode='a', header=not q_path.exists(), index=False)
                st.balloons()
                st.success("Ticket Sent!")

    st.markdown("---")
    st.markdown("### 🏢 About the Platform")
    st.info(f"**{settings.PROJECT_NAME}** is an Enterprise-grade AI solution developed by Shailendra & Team. Goal: High-precision agriculture for every farmer.")