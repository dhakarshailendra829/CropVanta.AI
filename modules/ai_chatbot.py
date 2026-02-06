import streamlit as st
import pandas as pd
import os
from datetime import datetime

class AIChatbot:
    def __init__(self, kb_path="data/chatbot_kb.csv"):
        self.kb_path = kb_path
        self.default_response = " I'm sorry, I couldn't find an answer to that. Would you like to ask about Agriculture, Mandi rates, or Seeds instead?"
        self.load_kb()

    def load_kb(self):
        if os.path.exists(self.kb_path):
            self.kb_df = pd.read_csv(self.kb_path)
            self.kb_df['keyword'] = self.kb_df['keyword'].str.lower()
        else:
            self.kb_df = pd.DataFrame(columns=['keyword', 'answer'])

    def get_response(self, query):
        query = query.lower().strip()
        
        for _, row in self.kb_df.iterrows():
            keywords = [k.strip() for k in str(row['keyword']).split(',')]
            if any(k in query for k in keywords):
                return row['answer']
        
        return self.default_response

def run():
    st.markdown("""
        <style>
        .stChatFloatingInputContainer { background-color: #0e1117 !important; }
        .bot-msg { background: #1e293b; padding: 15px; border-radius: 15px; border-left: 5px solid #00fbff; margin: 10px 0; color: #e2e8f0; }
        .user-msg { background: #0f172a; padding: 15px; border-radius: 15px; border-right: 5px solid #FF0080; text-align: right; margin: 10px 0; color: #ffffff; }
        </style>
    """, unsafe_allow_html=True)

    bot = AIChatbot()

    st.title("CropVanta AI Support")
    st.caption("Powered by Local Knowledge Base | 2026 Stable")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "bot", "content": "Namaste! I'm CropVanta AI Assistant . I can help you about soil test, crop recommendation, Crop prices etc."}]

    for msg in st.session_state.messages:
        div_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        st.markdown(f"<div class='{div_class}'>{msg['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Please Write Your Questions... (e.g., Wheat price, Soil help)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        response = bot.get_response(prompt)
        st.session_state.messages.append({"role": "bot", "content": response})
        
        st.rerun()

    with st.sidebar:
        st.markdown("### 💡 Quick Help")
        if st.button("🌾 Wheat Cultivation"):
            st.session_state.messages.append({"role": "user", "content": "Wheat cultivation"})
            st.rerun()
        if st.button("💰 Current Mandi Rates"):
            st.session_state.messages.append({"role": "user", "content": "mandi rates"})
            st.rerun()