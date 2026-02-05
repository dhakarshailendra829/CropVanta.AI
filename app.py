import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import random
from datetime import datetime
from pathlib import Path
from PIL import Image
from streamlit_autorefresh import st_autorefresh

from modules.core.config import settings
from modules.core.logger import get_logger
from modules.core.schemas import CropInput
from modules.core.auth import check_password  

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

logger = get_logger("CropVanta_Main")

st.set_page_config(
    page_title=f"🌾 {settings.PROJECT_NAME}",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f: 
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_modern_css()  
local_css("styles.css")  

# Ensure Directories exist
for path in ["uploaded_papers", "data/feedback", "logs"]:
    Path(path).mkdir(parents=True, exist_ok=True)

@st.cache_resource
def init_services():
    try:
        scaler = joblib.load(settings.SCALER_PATH)
        model = joblib.load(settings.MODEL_PATH)
        logger.info("Resources loaded successfully.")
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
        df = pd.read_csv("data/mandi_prices.csv", encoding="utf-8")
        return df
    except: 
        return pd.DataFrame()

market_df = load_market_data()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329115.png", width=80)
    st.markdown(f"### {settings.PROJECT_NAME} Admin")
    if st.checkbox("🔐 Admin Portal"):
        if check_password():
            st.success("Admin Access Granted")
            if st.button("Clear Logs"):
                open("logs/app.log", "w").close()
                st.info("Logs cleared.")
    st.markdown("---")
    st.info(f"Version: {settings.VERSION}")

st.markdown(f"<h1 class='main-title'>🌾 {settings.PROJECT_NAME}</h1>", unsafe_allow_html=True)

tabs = st.tabs([
    "📊 Dashboard", "🌱 Crop AI", "🌍 Land Suitability", 
    "📈 Market & Calendar", "📚 Research Portal", "🤖 AI Assistant", "👥 Community"
])

# --- TAB 0: DASHBOARD ---
with tabs[0]:
    st_autorefresh(interval=10000, key="dashboard_refresh") 

    st.markdown("""<div style='background: rgba(46, 204, 113, 0.1); padding: 10px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #2ecc71;'><marquee behavior="scroll" direction="left" style='color: #2ecc71; font-weight: bold;'>🌾 Rabi Sowing Target Achieved: 102% | 🚜 New Subsidy on Solar Pumps Announced | 📈 Organic Wheat Exports Up by 14% | 🌦️ El Niño impact weakening for 2026 Monsoon.</marquee></div>""", unsafe_allow_html=True)

    now = datetime.now()
    hour = now.hour
    if hour < 12:
        emoji, greeting, bg_grad = "🌅", "Good Morning", "linear-gradient(135deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%)"
    elif hour < 18:
        emoji, greeting, bg_grad = "☀️", "Good Afternoon", "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)"
    else:
        emoji, greeting, bg_grad = "🌙", "Good Evening", "linear-gradient(135deg, #2c3e50 0%, #000000 100%)"
    
    st.markdown(f"""
        <div style='background: {bg_grad}; padding: 40px; border-radius: 25px; border: 1px solid #334155; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);'>
            <h1 style='font-size: 3.5rem; margin:0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                {emoji} {greeting}, Shailendra!
            </h1>
            <p style='color: #f1f5f9; font-size: 1.3rem; margin-top: 10px; opacity: 0.9;'>CropVanta AI: Mission Control 2026</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 National Crop Production Trends")
    chart_data = pd.DataFrame({
        'Year': ['2021', '2022', '2023', '2024', '2025', '2026 (Est)'],
        'Rice': [124, 129, 132, 135, 138, 142],
        'Wheat': [109, 107, 110, 112, 115, 118]
    }).set_index('Year')
    st.area_chart(chart_data, color=["#00fbff", "#2ecc71"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Soil Health Index", "8.4/10", "Optimal")
    with c2: st.metric("Avg. Yield/Acre", "22.5 Qt", "+1.2%")
    with c3: st.metric("Diesel Price", "₹89.4", "-₹2.1")
    with c4: st.metric("Market Demand", "High", "Wheat")

    st.markdown("---")
    col_img, col_quote = st.columns([1, 2])
    quotes = [
        "Agriculture is our wisest pursuit, contributing most to real wealth and morals.",
        "The farmer is the only man who buys retail, sells wholesale, and pays the freight.",
        "To a farmer, the dirt is not just soil, it's hope."
    ]
    with col_img:
        st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80", 
                 caption="Precision Farming 2026", use_container_width=True)
    with col_quote:
        st.markdown(f"<div style='background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 20px; border-left: 10px solid #2ecc71; height: 100%; display: flex; align-items: center;'><h2 style='color: #f8fafc; font-style: italic;'>\"{random.choice(quotes)}\"</h2></div>", unsafe_allow_html=True)

# --- TAB 1: CROP AI ---
with tabs[1]:
    st.subheader("🌱 Precision Crop Recommendation")
    if 'last_result' not in st.session_state: st.session_state.last_result = None

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
        submit = st.form_submit_button("Run AI Analysis")

    if submit and services:
        with st.spinner("🤖 AI analyzing soil and fetching 2026 research..."):
            try:
                v_input = CropInput(nitrogen=N, phosphorus=P, potassium=K, temperature=temp, humidity=60.0, ph=ph, rainfall=rain)
                st.session_state.last_result = services["advisor"].recommend_crop(v_input)
            except Exception as e:
                st.error(f"Prediction Error: {e}")

    if st.session_state.last_result:
        res = st.session_state.last_result
        if res["status"] == "success":
            st.balloons()
            st.markdown(f"""
                <div style='background: rgba(46, 204, 113, 0.1); padding: 25px; border-radius: 15px; border: 1px solid #2ecc71;'>
                    <h2 style='color: #2ecc71;'>✅ Recommended: {res['crop_name']}</h2>
                    <p style='font-size: 1.1rem;'><b>AI Confidence:</b> {res['confidence_score']}%</p>
                    <hr style='border-color: #2ecc71;'>
                    <h4>🔬 2026 Research Insights:</h4>
                    <div style='color: #cbd5e1;'>{res['description']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- TAB 3: MARKET ---
with tabs[3]:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 📈 Market Insights")
        if not market_df.empty:
            sel_state = st.selectbox("Select State", market_df['state'].unique())
            crop_q = st.text_input("Search Crop Price", "Wheat")
            analysis = services["market"].process_market_data(market_df, crop_q, sel_state)
            if analysis.get("status") == "success":
                st.info(f"Market Sentiment: **{analysis['insights'].get('trend_sentiment')}**")
                st.dataframe(analysis["data"], use_container_width=True)
            else:
                st.warning(f"No data for '{crop_q}' in {sel_state}. Showing generic listings.")
                st.dataframe(market_df.head(10), use_container_width=True)
    with c2:
        st.markdown("### 🗓 Crop Calendar")
        if services["calendar"]: st.dataframe(services["calendar"].get_calendar_df(), use_container_width=True)

# --- TAB 6: COMMUNITY ---
with tabs[6]:
    st.markdown("<h2 style='color: #FF0080; text-align: center;'>👥 Farmer Community Hub</h2>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1.5, 1])
    f_path = Path("data/feedback.csv")
    
    with col_b:
        st.markdown("### ✍️ Post an Update")
        with st.form("community_post", clear_on_submit=True):
            u_name = st.text_input("Name/Region")
            u_msg = st.text_area("Share a tip")
            if st.form_submit_button("Post"):
                new_data = pd.DataFrame([[u_name, u_msg, datetime.now().strftime("%Y-%m-%d %H:%M")]], columns=["User", "Message", "Date"])
                if f_path.exists(): new_data.to_csv(f_path, mode='a', header=False, index=False)
                else: new_data.to_csv(f_path, index=False)
                st.success("Shared with community!")
                st.rerun()

    with col_a:
        st.markdown("### 💬 Recent Discussions")
        if f_path.exists():
            fb_df = pd.read_csv(f_path).iloc[::-1]
            for _, row in fb_df.head(10).iterrows():
                st.markdown(f"""<div style='background: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #FF0080; margin-bottom: 10px;'>
                    <h4 style='margin:0;'>👤 {row['User']}</h4><small>{row['Date']}</small><p>{row['Message']}</p></div>""", unsafe_allow_html=True)

with tabs[2]: land_suitability.run()
with tabs[4]: 
    papers = services["papers"].get_papers()
    if papers:
        for p in papers:
            with st.expander(f"📖 {p['Title']}"): display_pdf(services["papers"].get_paper_path(p['Filename']))
with tabs[5]: ai_chatbot.run()

st.markdown("---")
st.caption(f"CropVanta AI | {settings.VERSION} | {datetime.now().year}")