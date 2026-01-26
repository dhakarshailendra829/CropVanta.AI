import streamlit as st
import os
st.set_page_config(page_title="About", layout="wide")
st.title("About This Platform")
st.markdown("""
<style>
    .about-container { padding: 10px 40px; }
    
    .about-title {
        font-size: 3.2rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #00fbff, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .about-desc {
        font-size: 1.15rem;
        color: #cbd5e1;
        line-height: 1.8;
        margin-bottom: 25px;
    }

    .engineer-badge {
        display: inline-block;
        background: rgba(79, 172, 254, 0.1);
        border: 1px solid #4facfe;
        color: #4facfe;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }

    .styled-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 25px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="about-container">', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown('<div class="engineer-badge">Solo-Engineer Initiative</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="about-title">About the Platform</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p class="about-desc">
    <b>CropVanta.AI </b> is an independent, open-source project conceived and developed by a 
    <b>AI/ML Software Engineer Student</b> with a vision to transform traditional farming. 
    Unlike corporate tools, this platform is built on the principles of transparency and 
    technical excellence, ensuring that advanced machine learning models are accessible 
    to every farmer without any cost.
    </p>
    """, unsafe_allow_html=True)
    
    st.info("💡 **True Open Source:** Every line of code, from the Neural Networks to the UI, is crafted to empower the agricultural community.")

with col2:
    if os.path.exists("images/engineer_vision.png"):
        st.image("images/engineer_vision.png", use_container_width=True)
    else:
        st.markdown('<div style="background: #0f172a; height:320px; border-radius:25px; border:1px solid rgba(0,251,255,0.2); display:flex; align-items:center; justify-content:center; color:#64748b; text-align:center; padding:20px;">[Engineer Vision Image: images/engineer_vision.png]</div>', unsafe_allow_html=True)

st.markdown('<div style="margin-top: 80px;"></div>', unsafe_allow_html=True)

col3, col4 = st.columns([1, 1.2], gap="large")

with col3:
    if os.path.exists("images/platform_logic.png"):
        st.image("images/platform_logic.png", use_container_width=True)
    else:
        st.markdown('<div style="background: #0f172a; height:320px; border-radius:25px; border:1px solid rgba(79, 172, 254, 0.2); display:flex; align-items:center; justify-content:center; color:#64748b; text-align:center; padding:20px;">[Platform Workflow Image: images/platform_logic.png]</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="styled-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#ffffff; margin-top:0;">Built for Accuracy & Scale</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p class="about-desc">
    The core of this platform integrates high-precision <b>Random Forest Classifiers</b>, 
    real-time <b>Mandi API data</b>, and geospatial mapping. By combining Data Science 
    expertise with a passion for social impact, I have designed this platform to be 
    scalable, fast, and highly intuitive. 
    <br><br>
    As an AI/ML Engineer, my goal is to bridge the gap between complex research and 
    practical field-level implementation.
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)