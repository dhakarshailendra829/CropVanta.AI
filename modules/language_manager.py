import streamlit as st

def get_translations():
    return {
        'English': {
            'nav_dashboard': '📊 Dashboard', 'nav_crop_ai': '🌱 Crop AI', 'nav_land': '🌍 Land',
            'nav_market': '📈 Market', 'nav_research': '📚 Research', 'nav_assistant': '🤖 Assistant',
            'nav_community': '👥 Community', 'nav_planner': '🚀 Pro Planner',
            'welcome': 'Welcome, Shailendra!', 'tagline': 'CropVanta AI: Mission Control 2026',
            'post_btn': 'Post an Update', 'analysis_btn': '🚀 RUN AI ANALYSIS',
            'insight_header': 'AI Smart Insights', 'risk_level': 'Risk Assessment',
            'soil_n': 'Nitrogen (N)', 'soil_p': 'Phosphorus (P)', 'soil_k': 'Potassium (K)',
            'soil_temp': 'Temp (°C)', 'soil_ph': 'pH', 'soil_rain': 'Rain (mm)',
            'res_header': 'AI Recommendation',
            'conf_score': 'Confidence Score'  
        },
        'Hindi': {
            'nav_dashboard': '📊 डैशबोर्ड', 'nav_crop_ai': '🌱 फसल AI', 'nav_land': '🌍 भूमि',
            'nav_market': '📈 बाजार', 'nav_research': '📚 अनुसंधान', 'nav_assistant': '🤖 सहायक',
            'nav_community': '👥 समुदाय', 'nav_planner': ' प्रो प्लानर',
            'welcome': 'स्वागत है, शैलेंद्र!', 'tagline': 'क्रॉपवांटा AI: मिशन कंट्रोल 2026',
            'post_btn': 'अपडेट पोस्ट करें', 'analysis_btn': ' AI विश्लेषण',
            'insight_header': 'AI स्मार्ट जानकारी', 'risk_level': 'जोखिम मूल्यांकन',
            'soil_n': 'नाइट्रोजन (N)', 'soil_p': 'फास्फोरस (P)', 'soil_k': 'पोटेशियम (K)',
            'soil_temp': 'तापमान (°C)', 'soil_ph': 'pH', 'soil_rain': 'वर्षा (mm)',
            'res_header': 'AI की सिफारिश',
            'conf_score': 'भरोसा स्कोर'  
        },
        'Punjabi': {
            'nav_dashboard': '📊 ਡੈਸ਼ਬੋਰਡ', 'nav_crop_ai': '🌱 ਫਸਲ AI', 'nav_land': '🌍 ਜ਼ਮੀਨ',
            'nav_market': '📈 ਮੰਡੀ', 'nav_research': '📚 ਖੋਜ', 'nav_assistant': '🤖 ਸਹਾਇਕ',
            'nav_community': '👥 ਭਾਈਚਾਰਾ', 'nav_planner': ' ਪ੍ਰੋ ਪਲਾਨਰ',
            'welcome': 'ਜੀ ਆਇਆਂ ਨੂੰ, ਸ਼ੈਲੇਂਦਰ!', 'tagline': 'ਕਰੋਪਵਾਂਟਾ AI: ਮਿਸ਼ਨ ਕੰਟਰੋਲ 2026',
            'post_btn': 'ਅਪਡੇਟ ਪੋਸਟ ਕਰੋ', 'analysis_btn': ' AI ਵਿਸ਼ਲੇਸ਼ਣ',
            'insight_header': 'AI ਸਮਾਰਟ ਜਾਣਕਾਰੀ', 'risk_level': 'ਜੋਖਮ ਮੁਲਾਂਕਣ',
            'soil_n': 'ਨਾਈਟ੍ਰੋਜਨ (N)', 'soil_p': 'ਫਾਸਫੋਰਸ (P)', 'soil_k': 'ਪੋਟਾਸ਼ੀਅਮ (K)',
            'soil_temp': 'ਤਾਪਮਾਨ (°C)', 'soil_ph': 'pH', 'soil_rain': 'ਵਰਖਾ (mm)',
            'res_header': 'AI ਸਿਫਾਰਸ਼',
            'conf_score': 'ਭਰੋਸਾ ਸਕੋਰ' 
        },
        'Chinese': {
            'nav_dashboard': '📊 仪表板', 'nav_crop_ai': '🌱 AI 作物', 'nav_land': '🌍 土地',
            'nav_market': '📈 市场', 'nav_research': '📚 研究', 'nav_assistant': '🤖 助手',
            'nav_community': '👥 社区', 'nav_planner': ' 专业规划',
            'welcome': '欢迎, Shailendra!', 'tagline': 'CropVanta AI: 2026 任务控制',
            'post_btn': '发布更新', 'analysis_btn': ' 运行分析',
            'insight_header': 'AI 智能见解', 'risk_level': '风险评估',
            'soil_n': '氮 (N)', 'soil_p': '磷 (P)', 'soil_k': '钾 (K)',
            'soil_temp': '温度', 'soil_ph': 'pH', 'soil_rain': '降雨',
            'res_header': 'AI 建议',
            'conf_score': '置信度'  
        }
    }