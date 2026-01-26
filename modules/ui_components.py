import streamlit as st
import base64
import os

def load_modern_css():
    """Injects ultra-modern glassmorphism CSS for the Enterprise Look."""
    st.markdown("""
    <style>
    /* Global Styles for Dark Theme Consistency */
    .stApp { background-color: #0e1117; }
    
    /* Modern Glassmorphism Card */
    .agri-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .agri-card:hover {
        transform: translateY(-5px);
        border-color: #2ecc71;
    }
    
    /* Typography */
    .card-title { color: #2ecc71; font-weight: 700; font-size: 1.4rem; margin-bottom: 8px; }
    .card-meta { color: #94a3b8; font-size: 0.9rem; }
    
    /* PDF Viewer Container */
    .pdf-container {
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid #2ecc71;
    }

    /* Feedback Style */
    .feedback-bubble {
        background: #1e293b;
        border-radius: 15px;
        padding: 15px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def display_pdf(file_path: str):
    """Encodes a PDF file to Base64 and displays it in an Iframe."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # Embedding PDF in HTML Iframe
            pdf_html = f'''
            <div style="border: 3px solid #00fbff; border-radius: 20px; padding: 10px; background: #1a1a1a; box-shadow: 0 0 30px rgba(0, 251, 255, 0.2);">
                <iframe src="data:application/pdf;base64,{base64_pdf}" 
                        width="100%" height="800" style="border-radius: 15px;">
                </iframe>
            </div>
        '''
            st.markdown(pdf_html, unsafe_allow_html=True)
        else:
            st.error("File not found on server.")
    except Exception as e:
        st.error(f"Could not display PDF: {e}")

def render_weather_stats(city: str, temp: float, humidity: float):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); 
                padding: 25px; border-radius: 20px; text-align: center; color: white;">
        <h3 style="margin:0;">📍 {city}</h3>
        <h1 style="margin:10px 0; font-size:3.5rem;">{temp}°C</h1>
        <p style="opacity:0.9;">Humidity: {humidity}% | Sky: Clear</p>
    </div>
    """, unsafe_allow_html=True)

def render_paper_card(title: str, topic: str, uploader: str):
    st.markdown(f"""
    <div class="agri-card">
        <div class="card-title">📄 {title}</div>
        <div style="margin-bottom: 15px;">
            <span style="background:rgba(46, 204, 113, 0.2); color:#2ecc71; 
                         padding:5px 15px; border-radius:50px; font-size:0.8rem;">
                {topic}
            </span>
        </div>
        <div class="card-meta">Contributed by: <b>{uploader}</b></div>
    </div>
    """, unsafe_allow_html=True)

def render_feedback_post(user: str, date: str, message: str):
    st.markdown(f"""
    <div class="feedback-bubble">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <b style="color:#3b82f6;">👤 {user}</b>
            <small style="color:#64748b;">{date}</small>
        </div>
        <p style="color:#e2e8f0; margin:0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)