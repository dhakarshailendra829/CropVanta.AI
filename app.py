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
        with open(file_name, encoding="utf-8") as f: # <--- Very Important
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_modern_css()  
local_css("styles.css")  

# 📂 Fixed: Ensure correct directories exist
Path("uploaded_papers").mkdir(parents=True, exist_ok=True)
Path("data/feedback").mkdir(parents=True, exist_ok=True)

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
            "papers": PaperManager(upload_dir="uploaded_papers") 
        }
    except Exception as e:
        logger.error(f"Failed to load resources: {e}")
        return None

services = init_services()

@st.cache_data
def load_market_data():
    try: 
        # 🔥 FIXED: Added encoding to read mandi prices safely
        return pd.read_csv("data/mandi_prices.csv", encoding="utf-8")
    except: 
        return pd.DataFrame()

market_df = load_market_data()

# -------------------- Main Navigation --------------------
st.markdown(f"<h1 class='main-title'>🌾 {settings.PROJECT_NAME}</h1>", unsafe_allow_html=True)

tabs = st.tabs([
    "📊 Dashboard", "🌱 Crop AI", "🌍 Land Suitability", 
    "📈 Market & Calendar", "📚 Research Portal", "🤖 AI Assistant", "👥 Community"
])

# -------------------- Tab 0: Dashboard --------------------
with tabs[0]:
    st.markdown("""<div style='background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(0, 251, 255, 0.2);'><marquee behavior="scroll" direction="left" style='color: #00fbff; font-weight: bold;'>🌾 Wheat: ₹2,450/qtl ▲ | 🟢 Mustard: ₹5,600/qtl ▲ | 🍚 Rice: ₹3,100/qtl ▼ | ⚡ AI Engine: Stable | 🌦️ Weather Alert: High Yield Expected.</marquee></div>""", unsafe_allow_html=True)

    hour = datetime.now().hour
    greeting = "🌅 Good Morning" if hour < 12 else "☀️ Good Afternoon" if hour < 18 else "🌙 Good Evening"
    
    st.markdown(f"<div style='background: linear-gradient(90deg, #FF0080, #7928CA, #00fbff); padding: 2px; border-radius: 20px; margin-bottom: 25px;'><div style='background: #0e1117; padding: 35px; border-radius: 18px; text-align: center;'><h1 style='margin:0; background: linear-gradient(to right, #00fbff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{greeting}, Shailendra!</h1><p style='color: #94a3b8;'>Welcome back to AgroPulse AI Mission Control.</p></div></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("System Health", "98.8%", delta="Optimal")
    with c2: st.metric("AI Accuracy", "98.2%", delta="0.4% ▲")
    with c3: st.metric("Market Sentiment", "Bullish", delta="High")

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
            st.markdown(f"""
            <div class='agri-card' style='border-left: 5px solid #2ecc71;'>
                <h3>✅ Recommended: {result['crop_name']}</h3>
                <p><b>Confidence:</b> {result['confidence_score']}%</p>
                <p>{result['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.progress(int(float(result['confidence_score'])))

# -------------------- Tab 2: Land Suitability (FIXED MAP) --------------------
with tabs[2]:
    st.markdown("<h2 style='text-align: center; color: #00fbff;'>🌍 Land Suitability Mapping</h2>", unsafe_allow_html=True)
    
    # 🔥 FIXED: Map Visibility Hack - Specific Container
    map_container = st.container()
    with map_container:
        try:
            # We call the external module
            land_suitability.run() 
        except Exception as e:
            st.error(f"Map Display Error: {e}")

# -------------------- Tab 3: Market & Calendar (DYNAMIC) --------------------
with tabs[3]:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("<h3 style='color: #FFEE00;'>📈 Market Insights</h3>", unsafe_allow_html=True)
        # 🌍 FIXED: Dynamic State Selection from Market Data
        states = market_df['state'].unique().tolist() if not market_df.empty else ["Punjab"]
        selected_state = st.selectbox("Select State", states)
        crop_query = st.text_input("Search Crop Price", "Wheat")
        
        if not market_df.empty:
            analysis = services["market"].process_market_data(market_df, crop_query, selected_state)
            if analysis.get("status") == "success":
                st.dataframe(analysis["data"], use_container_width=True)
            else:
                st.warning(f"🔍 No live data for '{crop_query}' in {selected_state}. Try searching 'Rice' or 'Wheat'.")

    with c2:
        st.markdown("<h3 style='color: #00fbff;'>🗓 Crop Calendar</h3>", unsafe_allow_html=True)
        st.dataframe(services["calendar"].get_calendar_df(), use_container_width=True)

# -------------------- Tab 4: Research Portal (FIXED PATH) --------------------
with tabs[4]:
    st.subheader("📚 Digital Research Repository")
    papers_list = services["papers"].get_papers()
    if papers_list:
        for p in papers_list:
            with st.expander(f"📖 {p['Title']} ({p['Topic']})"):
                pdf_path = services["papers"].get_paper_path(p['Filename'])
                if pdf_path:
                    display_pdf(pdf_path)
                else:
                    st.error(f"File {p['Filename']} not found in uploaded_papers/")
    else:
        st.info("No papers available in the repository.")

# -------------------- Tab 5: AI Assistant --------------------
with tabs[5]:
    ai_chatbot.run()

# -------------------- Tab 6: Community & Support (RESTORED) --------------------
with tabs[6]:
    st.markdown("<h2 style='color: #FF0080; text-align: center;'>👥 Farmer Community Hub</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1.2, 1])
    
    with col_a:
        st.markdown("### 💬 Recent Discussions")
        feedback_container = st.container(height=500)
        with feedback_container:
            f_path = Path("data/feedback.csv")
            if f_path.exists():
                fb_df = pd.read_csv(f_path, encoding="utf-8")
                # 🔥 Show latest first
                for _, row in fb_df.iloc[::-1].iterrows(): 
                    st.markdown(f"""
                    <div style='background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #FF0080; margin-bottom: 15px;'>
                        <h4 style='margin:0; color: #FF0080;'>👤 {row['User']}</h4>
                        <small style='color: #94a3b8;'>📅 {row['Date']}</small>
                        <p style='margin-top: 10px; font-size: 1.1rem;'>{row['Message']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No discussions yet. Be the first to post!")

    with col_b:
        st.markdown("### ✍️ Post an Update")
        with st.form("community_post", clear_on_submit=True):
            user_name = st.text_input("Your Name/Region")
            message = st.text_area("Share a crop tip or feedback")
            submit_post = st.form_submit_button("📢 Post to Community")
            
            if submit_post and user_name and message:
                f_path = Path("data/feedback.csv")
                new_post = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), user_name, message]], 
                                      columns=["Date", "User", "Message"])
                new_post.to_csv(f_path, mode='a', header=not f_path.exists(), index=False)
                st.success("Post Shared!")
                st.rerun()

        st.markdown("---")
        st.markdown("### 🛡️ Need Help?")
        with st.expander("Technical Support"):
            st.write("📧 support@agropulse.ai | 📞 1800-AGRI-AI")