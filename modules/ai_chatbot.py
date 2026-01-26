import streamlit as st

def run():
    st.markdown("<h1 style='text-align: center; color: #2ecc71;'>🤖 AgroPulse AI Guide</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>How can I assist you today?</p>", unsafe_allow_html=True)
    st.markdown("---")

    # State management for navigation
    if "step" not in st.session_state:
        st.session_state.step = "main"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Helper function to reset chat
    def reset_chat():
        st.session_state.step = "main"
        st.rerun()

    # --- MAIN MENU ---
    if st.session_state.step == "main":
        st.chat_message("assistant").write("Hello! Welcome to AgroPulse Support. Please select a topic to get started:")
        
        c1, c2, c3 = st.columns(3)
        if c1.button("🛠️ Platform Issues", use_container_width=True):
            st.session_state.step = "issues"
            st.rerun()
        if c2.button("🌱 Crop Guidance", use_container_width=True):
            st.session_state.step = "guidance"
            st.rerun()
        if c3.button("📊 Market Queries", use_container_width=True):
            st.session_state.step = "market"
            st.rerun()

    # --- LEVEL 1: PLATFORM ISSUES ---
    elif st.session_state.step == "issues":
        st.chat_message("assistant").write("I'm sorry you're facing trouble. What specific issue are you experiencing?")
        
        sc1, sc2, sc3 = st.columns(3)
        if sc1.button("Login Problems"):
            st.info("**Solution:** Ensure you are using the correct credentials in the sidebar. Admin access is restricted to authorized users.")
        if sc2.button("Data Not Loading"):
            st.warning("**Solution:** Check your internet connection. If you're on a local server, ensure the CSV files in the 'data/' folder are present.")
        if sc3.button("App is Slow"):
            st.success("**Solution:** We use cached resources to stay fast. Try clearing your browser cache or restarting the app.")
        
        if st.button("⬅️ Back to Main Menu"): reset_chat()

    # --- LEVEL 1: CROP GUIDANCE ---
    elif st.session_state.step == "guidance":
        st.chat_message("assistant").write("AI Crop Guidance is my specialty. What would you like to know?")
        
        sc1, sc2, sc3 = st.columns(3)
        if sc1.button("How Prediction Works?"):
            st.info("**Explanation:** Our Random Forest model analyzes Soil (NPK), pH, and Weather (Temp/Rain) to suggest the best crop for your land.")
        if sc2.button("Inaccurate Results"):
            st.warning("**Solution:** Ensure the NPK values are entered correctly from a recent soil test report for 98% accuracy.")
        if sc3.button("New Crop Requests"):
            st.success("**Solution:** Currently we support 22 crops. New datasets are being trained for the next update (v2.1).")

        if st.button("⬅️ Back to Main Menu"): reset_chat()

    # --- LEVEL 1: MARKET QUERIES ---
    elif st.session_state.step == "market":
        st.chat_message("assistant").write("I can help you understand market trends and prices.")
        
        sc1, sc2, sc3 = st.columns(3)
        if sc1.button("Mandi Price Delay"):
            st.info("**Note:** Our Mandi data is updated periodically. For live prices, check the official 'Agmarknet' portal.")
        if sc2.button("State Not Found"):
            st.warning("**Solution:** Currently, our dataset focuses on major agricultural states like Punjab, Haryana, and UP.")
        if sc3.button("Price Forecasting"):
            st.success("**Coming Soon:** Historical trend analysis and price forecasting feature is in the Phase 4 roadmap.")

        if st.button("⬅️ Back to Main Menu"): reset_chat()

    # Footer for dynamic feel
    st.markdown("---")
    st.caption("AgroPulse Intelligent Support Engine | Version 2.0.0")