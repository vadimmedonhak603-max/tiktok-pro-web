import streamlit as st
import requests
import time

# Konfiguracja strony
st.set_page_config(page_title="TikTok PRO Global", layout="wide")

# Stylizacja Black & Neon
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c22 0%, #000000 100%); color: white; }
    header, footer {visibility: hidden;}
    .stTextArea textarea { background-color: #050505 !important; color: #00d4ff !important; border: 1px solid #00d4ff !important; border-radius: 12px; }
    .stButton>button { background: linear-gradient(145deg, #00d4ff, #0055ff) !important; color: white !important; font-weight: bold; border-radius: 30px; height: 3.5em; width: 100%; border: none; font-size: 16px; }
    iframe { background-color: transparent !important; border: none !important; }
    .stRadio label { color: white !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# WYBÓR JĘZYKA - 4 OPCJE (Widoczne na środku)
lang = st.radio("Select Language / Wybierz język / Виберіть мову:", ["PL", "EN", "UA", "RU"], horizontal=True)

# SŁOWNIK TŁUMACZEŃ
translations = {
    "PL": {"title": "🛡️ TikTok PRO Downloader", "step1": "📥 1. Wklej Linki", "step2": "📋 2. Gotowe", "start": "🚀 START", "ready": "Gotowe", "dl": "POBIERZ"},
    "EN": {"title": "🛡️ TikTok PRO Global", "step1": "📥 1. Paste Links", "step2": "📋 2. Ready", "start": "🚀 START", "ready": "Ready", "dl": "DOWNLOAD"},
    "UA": {"title": "🛡️ TikTok PRO Україна", "step1": "📥 1. Вставте посилання", "step2": "📋 2. Готово", "start": "🚀 СТАРТ", "ready": "Готово", "dl": "ЗАВАНТАЖИТИ"},
    "RU": {"title": "🛡️ TikTok PRO Россия", "step1": "📥 1. Вставьте ссылки", "step2": "📋 2. Готово", "start": "🚀 СТАРТ", "ready": "Готово", "dl": "СКАЧАТЬ"}
}

t = translations[lang]

st.title(t["title"])

if 'links' not in st.session_state:
    st.session_state.links = []

col_in, col_out = st.columns([1, 1])

with col_in:
    st.subheader(t["step1"])
    urls_input = st.text_area("URLs:", height=250, placeholder="TikTok links...")
    
    if st.button(t["start"]):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            results = []
            bar = st.progress(0)
            for i, url in enumerate(urls):
                try:
                    r = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                    if r.get('code') == 0:
                        results.append(r['data']['play'])
                    time.sleep(0.3)
                except: pass
                bar.progress((i + 1) / len(urls))
            st.session_state.links = results

with col_out:
    st.subheader(t["step2"])
    if st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            js_code = f"""
            <body style="background-color: transparent; margin: 0; padding: 0; display: flex; justify-content: space-between; align-items: center; overflow: hidden;">
                <span style="color: #28a745 !important; font-weight: bold; font-family: sans-serif; font-size: 14px;">Video #{i+1} {t['ready']}</span>
                <button onclick="dl()" style="background-color: #28a745; color: white; border: none; border-radius: 6px; padding: 6px 15px; font-weight: bold; cursor: pointer; font-size: 12px;">{t['dl']}</button>
                <script>function dl() {{ fetch('{link}').then(r => r.blob()).then(b => {{ const u = window.URL.createObjectURL(b); const a = document.createElement('a'); a.href = u; a.download = "video_{i+1}.mp4"; a.click(); }}); }}</script>
            </body>
            """
            st.components.v1.html(js_code, height=45)
# --- SEKCJA WSPARCIA (NA DOLE STRONY) ---
st.write("---")  # Linia oddzielająca
st.write("❤️ Support this project / Wesprzyj projekt")

# Ten blok usuwa duplikaty i tworzy jeden, klikalny przycisk na środku
st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <a href="https://www.buymeacoffee.com/waldAS" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
            alt="Buy Me A Coffee" 
            style="height: 60px !important; width: 217px !important;" >
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
