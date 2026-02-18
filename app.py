import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import requests
import random
from datetime import datetime
from pathlib import Path
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# 🔐 NEW AUTH IMPORTS
from modules.core.user_store import create_user, authenticate_user
from modules.core.auth import create_access_token

from modules.core.config import settings
from modules.core.logger import get_logger
from modules.core.schemas import CropInput
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
from modules.language_manager import get_translations

logger = get_logger("CropVanta_Main")
# ------------------ SESSION INIT ------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ------------------ PAGE CONFIG ------------------

st.set_page_config(
    page_title=f"🌾 {settings.PROJECT_NAME}",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ SIDEBAR ------------------

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329115.png", width=80)

    st.markdown("## 👤 Account")

    if not st.session_state.authenticated:

        auth_mode = st.radio("Select Option", ["Login", "Signup"])

        if auth_mode == "Signup":
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Create Account"):
                success, message = create_user(full_name, email, password)
                if success:
                    st.success("Account created. Please login.")
                else:
                    st.error(message)

        else:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                user = authenticate_user(email, password)
                if user:
                    token = create_access_token(
                        {"sub": user["email"], "role": user["role"]}
                    )
                    st.session_state.authenticated = True
                    st.session_state.user_email = user["email"]
                    st.session_state.user_role = user["role"]
                    st.session_state.jwt_token = token
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    else:
        st.success(f"Logged in as {st.session_state.user_email}")

        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    # 🔐 ROLE BASED ADMIN PANEL
    if st.session_state.get("user_role") == "admin":
        st.markdown("### 🛠 Admin Panel")

        if st.button("Clear Logs"):
            open("logs/app.log", "w").close()
            st.success("Logs Cleared")

    st.markdown("---")

    languages = get_translations()
    sel_lang = st.selectbox("🌐 Language / भाषा", list(languages.keys()))
    T = languages[sel_lang]

    st.info(f"Version: {settings.VERSION}")

# 🚫 STOP if not logged in
if not st.session_state.authenticated:
    st.warning("Please login to access CropVanta.AI SaaS Platform.")
    st.stop()

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f: 
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_modern_css()  
local_css("styles.css")  

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
if services is None:
    st.error("Critical system error. Please check model files.")
    st.stop()

@st.cache_data(ttl=3600)
def get_advanced_resources():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=22.71&longitude=75.85&hourly=shortwave_radiation,soil_moisture_3_to_9cm&daily=et0_fao_evapotranspiration&timezone=auto"
        res = requests.get(url).json()
        return {
            "sol": res['hourly']['shortwave_radiation'][0],
            "wat": res['daily']['et0_fao_evapotranspiration'][0],
            "mst": res['hourly']['soil_moisture_3_to_9cm'][0] * 100
        }
    except:
        return {"sol": 420, "wat": 4.5, "mst": 35.0} 

resource_data = get_advanced_resources()
s_sol = resource_data["sol"]
s_wat = resource_data["wat"]
s_moist = resource_data["mst"]
def load_market_data():
    try: 
        df = pd.read_csv("data/mandi_prices.csv", encoding="utf-8")
        return df
    except: 
        return pd.DataFrame()

market_df = load_market_data()
Path("data/community_images").mkdir(parents=True, exist_ok=True)

st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Rainbow Border Effect */
    .rainbow-container {
        background: linear-gradient(90deg, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #8B00FF);
        padding: 3px;
        border-radius: 25px;
        margin-bottom: 25px;
    }
    .rainbow-content {
        background: #161b22;
        padding: 30px;
        border-radius: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Metrics & Cards */
    div[data-testid="stMetric"] {
        background-color: #1c2128;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
    }
    div[data-testid="stMetricValue"] { color: #00fbff !important; }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #0e1117; gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1c2128;
        border-radius: 8px 8px 0 0;
        color: #8b949e;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #238636 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"<h1 style='color: #2ecc71; text-align: center; font-size: 3rem;'>🌾 {settings.PROJECT_NAME}</h1>", unsafe_allow_html=True)

tabs = st.tabs([
    T['nav_dashboard'], T['nav_crop_ai'], T['nav_land'], 
    T['nav_market'], T['nav_research'], T['nav_assistant'], T['nav_community'], T['nav_planner'], "Energy & Water AI"
])

with tabs[0]:
    st_autorefresh(interval=60000, key="dashboard_clock") 

    st.markdown("""<div style='background: rgba(46, 204, 113, 0.1); padding: 10px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #2ecc71;'><marquee behavior="scroll" direction="left" style='color: #2ecc71; font-weight: bold;'>🌾 Rabi Sowing Target Achieved: 102% | 🚜 New Subsidy on Solar Pumps Announced | 📈 Organic Wheat Exports Up by 14% | 🌦️ El Niño impact weakening for 2026 Monsoon.</marquee></div>""", unsafe_allow_html=True)

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d %b %Y")
    current_day = now.strftime("%A")

    st.markdown(f"""
        <div class="rainbow-container">
            <div class="rainbow-content">
                <div style='text-align: left;'>
                    <h1 style='font-size: 2.8rem; margin:0; color: white;'>{T['welcome']}</h1>
                    <p style='color: #8b949e; font-size: 1.2rem; margin-top: 5px;'>{T['tagline']}</p>
                </div>
                <div style='text-align: right;'>
                    <div style='color: #00fbff; font-family: "Courier New", monospace; font-size: 3rem; font-weight: bold; line-height: 1;'>{current_time}</div>
                    <div style='color: #ffffff; font-size: 1.1rem; margin-top: 5px;'>{current_day}, {current_date}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### National Crop Production Trends")
    chart_data = pd.DataFrame({
        'Year': ['2021', '2022', '2023', '2024', '2025', '2026 (Est)'],
        'Rice': [124, 129, 132, 135, 138, 142],
        'Wheat': [109, 107, 110, 112, 115, 118]
    }).set_index('Year')
    st.area_chart(chart_data, color=["#00ff1a", "#250a9e"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Soil Health", "8.4/10", "Optimal")
    with c2: st.metric("Avg. Yield", "22.5 Qt", "+1.2%")
    with c3: st.metric("Diesel Price", "₹89.4", "-₹2.1")
    with c4: st.metric("Demand", "High", "Wheat")

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
        import random
        st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 20px; 
            border-left: 10px solid #2ecc71; height: 100%; display: flex; align-items: center;'>
                <h2 style='color: #f8fafc; font-style: italic;'>"{random.choice(quotes)}"</h2>
            </div>
        """, unsafe_allow_html=True)
with tabs[1]:
    st.markdown(
        f"<h2 style='color: #00fbff; text-align: center; font-family: sans-serif;'>{T['nav_crop_ai']} - Precision Analysis</h2>",
        unsafe_allow_html=True
    )
    
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    if 'trigger_balloons' not in st.session_state:
        st.session_state.trigger_balloons = False

    with st.form("prediction_form", clear_on_submit=False):
        st.markdown(
            f"<p style='color: #8b949e; text-align: center;'>{T['tagline']}</p>",
            unsafe_allow_html=True
        )
        
        c1, c2, c3 = st.columns(3)
        with c1:
            N = st.number_input(T['soil_n'], 0, 140, 50, help="Nitrogen content in soil")
            P = st.number_input(T['soil_p'], 5, 145, 50, help="Phosphorus content in soil")
        with c2:
            K = st.number_input(T['soil_k'], 5, 205, 50, help="Potassium content in soil")
            temp = st.number_input(T['soil_temp'], 0.0, 50.0, 25.0)
        with c3:
            ph = st.number_input(T['soil_ph'], 0.0, 14.0, 6.5)
            rain = st.number_input(T['soil_rain'], 0.0, 1000.0, 100.0)
        
        col_btn, _ = st.columns([1, 2])
        with col_btn:
            submit = st.form_submit_button(T['analysis_btn'])

    if submit and services:
        with st.spinner("🧬 AI Analysis in progress..."):
            try:
                v_input = CropInput(
                    nitrogen=N,
                    phosphorus=P,
                    potassium=K,
                    temperature=temp,
                    humidity=65.0,
                    ph=ph,
                    rainfall=rain
                )
                
                st.session_state.last_result = services["advisor"].recommend_crop(v_input)
                
                if st.session_state.last_result.get("status") == "success":
                    st.session_state.trigger_balloons = True
            except Exception as e:
                st.error(f"Prediction Error: {e}")

    if st.session_state.last_result:

        res = st.session_state.last_result

        if res.get("status") == "success":

            st.divider()

            col1, col2 = st.columns([3,1])

            with col1:
                st.subheader(T.get('res_header', 'AI Recommendation'))
                st.title(res.get('crop_name', 'Analyzing...'))

            with col2:
                st.metric(
                    label=T.get('conf_score','Confidence'),
                    value=f"{res.get('confidence_score',0)}%"
                )

            st.divider()

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("### 🧪 AI Insights")
                st.write(res.get('description','No details available.'))

            with c2:
                st.markdown("### 🛡️ Smart Farmer Advice")
                st.write(f"• Optimal pH detected: {ph}")
                st.write(f"• Recommended Fertilizer: Based on N={N}")
                st.write(f"• Watering schedule: Based on {rain}mm rain")


with tabs[3]:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### Market Insights")
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
        st.markdown("### Crop Calendar")
        if services["calendar"]: st.dataframe(services["calendar"].get_calendar_df(), use_container_width=True)
with tabs[6]:

    st.markdown(f"""
        <div style='background: linear-gradient(90deg, #FF0080, #8B00FF); padding: 15px; border-radius: 15px; margin-bottom: 25px;'>
            <h2 style='color: white; text-align: center; margin:0;'> {T['nav_community']}</h2>
        </div>
    """, unsafe_allow_html=True)

    f_path = Path("data/feedback.csv")
    img_folder = Path("data/community_images")
    img_folder.mkdir(parents=True, exist_ok=True)

    # Ensure CSV exists
    if not f_path.exists():
        pd.DataFrame(
            columns=["User", "Message", "Image", "Date"]
        ).to_csv(f_path, index=False)

    col_feed, col_post = st.columns([1.6, 1], gap="large")

    # ==========================
    # ✍️ POST SECTION
    # ==========================
    with col_post:
        st.markdown(
            f"<h3 style='color: #FF0080;'>✍️ {T['post_btn']}</h3>",
            unsafe_allow_html=True
        )

        with st.form("community_post", clear_on_submit=True):

            u_msg = st.text_area("What's on your mind?")
            u_img = st.file_uploader(
                "Add Photo",
                type=['jpg', 'png', 'jpeg']
            )

            if st.form_submit_button("Post to Community"):

                if u_msg.strip():

                    img_path = ""

                    if u_img:
                        img_filename = (
                            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{u_img.name}"
                        )
                        img_path = str(img_folder / img_filename)

                        with open(img_path, "wb") as f:
                            f.write(u_img.getbuffer())

                    new_entry = pd.DataFrame([[
                        st.session_state.user_email,
                        u_msg.strip(),
                        img_path,
                        datetime.now().strftime("%Y-%m-%d %H:%M")
                    ]], columns=["User", "Message", "Image", "Date"])

                    new_entry.to_csv(
                        f_path,
                        mode='a',
                        header=False,
                        index=False
                    )

                    st.success("Posted successfully!")
                    st.rerun()

                else:
                    st.error("Message cannot be empty.")

    # ==========================
    # 💬 FEED SECTION
    # ==========================
    with col_feed:

        st.markdown(
            "<h3 style='color: #8B00FF;'>💬 Recent Discussions</h3>",
            unsafe_allow_html=True
        )

        try:
            fb_df = pd.read_csv(f_path)

            if fb_df.empty:
                st.info("No posts yet. Start the conversation!")

            else:
                fb_df = fb_df.fillna("").iloc[::-1]

                for index, row in fb_df.iterrows():

                    with st.container(border=True):

                        c_text, c_img = st.columns([3, 1])

                        # Post Content
                        with c_text:
                            st.markdown(f"""
                                <span style='color: #FF0080; font-weight: bold;'>
                                    👤 {row['User']}
                                </span>
                                <p style='color: #e2e8f0; margin-top:5px;'>
                                    {row['Message']}
                                </p>
                                <small style='color: #8b949e;'>
                                    📅 {row['Date']}
                                </small>
                            """, unsafe_allow_html=True)

                        # Post Image
                        with c_img:
                            if row['Image'] and os.path.exists(str(row['Image'])):
                                st.image(
                                    row['Image'],
                                    use_container_width=True
                                )
                            else:
                                st.markdown("""
                                    <div style='height: 60px;
                                                background: #1c2128;
                                                border-radius: 10px;
                                                border: 1px dashed #334155;'>
                                    </div>
                                """, unsafe_allow_html=True)

                        # ==========================
                        # 🔐 ROLE-BASED DELETE
                        # ==========================

                        can_delete = (
                            st.session_state.user_role == "admin"
                            or row["User"] == st.session_state.user_email
                        )

                        if can_delete:
                            if st.button("🗑️ Delete", key=f"del_{index}"):

                                # Remove image if exists
                                if row['Image'] and os.path.exists(str(row['Image'])):
                                    try:
                                        os.remove(row['Image'])
                                    except:
                                        pass

                                actual_df = pd.read_csv(f_path)

                                # Safe drop
                                actual_df = actual_df.drop(
                                    actual_df.index[index]
                                )

                                actual_df.to_csv(f_path, index=False)

                                st.success("Post deleted.")
                                st.rerun()

        except Exception:
            st.warning("Resetting community feed structure...")
            pd.DataFrame(
                columns=["User", "Message", "Image", "Date"]
            ).to_csv(f_path, index=False)
            st.rerun()

with tabs[7 if len(tabs)>7 else 1]: 
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); padding: 25px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(168,85,247,0.3);'>
            <h2 style='color: white; text-align: center; margin:0;'> {T.get('nav_planner', 'Pro Planner')}</h2>
            <p style='color: #e8d5ff; text-align: center; margin-top: 5px;'>2026 Advanced Yield Prediction & Profit Analysis</p>
        </div>
    """, unsafe_allow_html=True)

    col_calc, col_viz = st.columns([1, 1.2], gap="large")

    with col_calc:
        st.markdown(f"<h4 style='color: #a855f7;'> {T.get('insight_header', 'Economic Forecast')}</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            acres = st.slider("Farm Size (Acres)", 1, 50, 5)
            budget = st.number_input("Input Budget (₹)", value=10000)
            target_crop = st.selectbox("Select Target Crop", ["Basmati Rice", "Sharbati Wheat", "Organic Mustard"])
            
            multiplier = 2.4 if "Organic" in target_crop else 1.8
            est_profit = (budget * multiplier) * acres
            
            st.markdown(f"""
                <div style='background: rgba(168,85,247,0.1); padding: 20px; border-radius: 15px; border: 1px solid #a855f7; text-align: center;'>
                    <span style='color: #8b949e;'>Estimated Net Profit</span>
                    <h1 style='color: #00fbff; margin:0;'>₹{est_profit:,.0f}</h1>
                    <small style='color: #2ecc71;'>ROI: +{int((multiplier-1)*100)}% based on market demand</small>
                </div>
            """, unsafe_allow_html=True)

    with col_viz:
        st.markdown(f"<h4 style='color: #6366f1;'> {T.get('risk_level', 'Real-time Risk Meter')}</h4>", unsafe_allow_html=True)
        
        risk_val = 22 
        st.progress(risk_val/100)
        st.write(f"Current Environment Risk: **{risk_val}% (Low)**")
        
        st.markdown(f"""
            <div style='background: #161b22; padding: 20px; border-radius: 15px; border-left: 5px solid #6366f1; margin-top: 15px;'>
                <p style='color: white; margin:0;'><b>💡 AI Smart Tip:</b></p>
                <p style='color: #8b949e; font-size: 0.9rem;'>
                    Mandi prices for {target_crop} are trending upwards. Consider using hermetic storage to sell in late Q3 for a 15% higher profit margin.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        m1, m2 = st.columns(2)
        m1.metric("Market Sentiment", "Bullish")
        m2.metric("Pest Probability", "Low 🛡️")

    st.toast("Pro Planner Insights Updated!", icon="💡")
with tabs[8]:
    solar_kwh = (s_sol * 5.5) / 1000 
    carbon_offset = solar_kwh * 0.85 

    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #065f46 0%, #064e3b 100%); 
                    padding: 30px; border-radius: 25px; border-bottom: 5px solid #10b981;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.4); text-align: center;'>
            <h1 style='color: #10b981; margin:0;'>⚡ Eco-Harvest Intelligence</h1>
            <p style='color: #a7f3d0; opacity: 0.9;'>Carbon Credits | Solar Pumping | Smart Irrigation</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("##")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Solar Potential", f"{s_sol} W/m²", "Optimal")
        st.write("☀️ **Status:** High PV Yield")
    with col2:
        st.metric("Water Evaporation", f"{s_wat} mm", "Alert", delta_color="inverse")
        st.write("💧 **Status:** High Soil Stress")
    with col3:
        st.metric("Carbon Saved", f"{carbon_offset:.2f} kg", "Green Credit")
        st.write("🌳 **Status:** Planet Positive")

    st.write("---")

    c_graph, c_advice = st.columns([2, 1])
    
    with c_graph:
        st.subheader("Energy-Water Synergy Graph")
        
        synergy_data = pd.DataFrame({
            'Solar Energy (kWh)': [1.1, 3.8, 8.2, 7.1, 2.5, 0.2],
            'Water Need (Liters)': [35, 15, 5, 20, 55, 40]
        }, index=['6am', '9am', '12pm', '3pm', '6pm', '9pm'])
        st.line_chart(synergy_data, color=["#fbbf24", "#3b82f6"])

    with c_advice:
        st.subheader("AI Automation")
        st.toggle("Smart Pump Scheduler", value=True)
        st.toggle("VPD Stress Alert", value=False)
        
        st.info(f"**Financial ROI:** Today's Solar harvest saved you **₹{solar_kwh * 7.2:.2f}** in electricity costs.")

    st.success(f" **Action Plan:** Solar intensity is at {s_sol} W/m². We recommend running the irrigation system between 11:30 AM and 2:00 PM to use 100% free energy.")
with tabs[2]: land_suitability.run()
with tabs[4]: 
    papers = services["papers"].get_papers()
    if papers:
        for p in papers:
            with st.expander(f" {p['Title']}"): display_pdf(services["papers"].get_paper_path(p['Filename']))
with tabs[5]: ai_chatbot.run()

st.markdown("---")
st.caption(f"CropVanta AI | {settings.VERSION} | {datetime.now().year}")