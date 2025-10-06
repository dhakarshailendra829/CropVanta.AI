import streamlit as st

def load_css():
    css = """
    <style>
    body { background-color: #f0f2f6; font-family: 'Segoe UI', sans-serif; }
    .main-header { text-align: center; padding: 15px; }
    .logo { height: 60px; margin-bottom: 10px; }
    .section-title { font-size: 22px; font-weight: bold; margin-bottom: 15px; color: #2c3e50; }
    
    /* Community post cards */
    .post-card { padding: 12px; margin-bottom: 10px; border-radius: 10px;
                 box-shadow: 2px 2px 6px rgba(0,0,0,0.1); color: #fff; }
    .post-card:nth-child(odd) { background: #3498db; }
    .post-card:nth-child(even) { background: #2ecc71; }
    .post-name { font-weight: bold; font-size: 16px; }
    .post-location { font-style: italic; font-size: 14px; }
    .post-message { margin-top: 5px; font-size: 15px; }
    .post-date { font-size: 12px; color: #ecf0f1; margin-top: 5px; }
    
    .weather-card { background: #eaf2f8; padding: 15px; border-radius: 10px; margin: 10px 0;
                    box-shadow: 2px 2px 8px rgba(0,0,0,0.1); }
    .weather-title { font-weight: bold; font-size: 18px; margin-bottom: 5px; color: #1f618d; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def show_weather_card(forecast):
    """Display weather nicely in the app."""
    st.markdown(f"""
    <div class="weather-card">
        <div class="weather-title">📍 {forecast['Location']} - {forecast['Date']}</div>
        <p>Max Temp: {forecast.get('Max Temp (°C)', forecast.get('Predicted Temp (°C)','N/A'))} °C</p>
        <p>Min Temp: {forecast.get('Min Temp (°C)','N/A')} °C</p>
        <p>Precipitation: {forecast.get('Precipitation (mm)','N/A')} mm</p>
        <p>Source: {forecast.get('Source','Unknown')}</p>
        <small>{forecast.get('Note','')}</small>
    </div>
    """, unsafe_allow_html=True)

def show_community_posts(posts_df):
    """Display all community posts in colorful cards."""
    for idx, row in posts_df[::-1].iterrows(): 
        st.markdown(f"""
        <div class="post-card">
            <div class="post-name">{row['Name']}</div>
            <div class="post-location">from {row['Location']}</div>
            <div class="post-message">{row['Message']}</div>
            <div class="post-date">🕒 {row['Date']}</div>
        </div>
        """, unsafe_allow_html=True)
