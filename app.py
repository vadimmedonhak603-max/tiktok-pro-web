import streamlit as st
import requests
import time

st.set_page_config(page_title="TikTok PRO Global", layout="wide")

# Stylizacja Black & Neon
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c22 0%, #000000 100%); color: white; }
    header, footer {visibility: hidden;}
    .stTextArea textarea { background-color: #050505 !important; color: #00d4ff !important; border: 1px solid #00d4ff !important; border-radius: 12px; }
    .stButton>button { background: linear-gradient(145deg, #00d4ff, #0055ff) !important; color: white !important; font-weight: bold; border-radius: 30px; height: 3.5em; width: 100%; border: none; }
    iframe { background-color: transparent !important; border: none !important; }
    .stRadio label { color: white !important; font-weight: bold !important; }
    /* Styl dla sekcji kawy na dole */
    .coffee-container { text-align: center; padding: 40px; margin-top: 50px; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# WYBÓR JĘZYKA
lang = st.radio("Language / Język / Мова:", ["PL", "EN", "UA", "RU"], horizontal=True)

translations = {
    "PL": {"title": "🛡️ TikTok PRO Downloader", "step1": "📥 1. Wklej Linki", "step2": "📋 2. Gotowe", "start": "🚀 START", "ready": "Gotowe", "dl": "POBIERZ", "support": "Wesprzyj projekt"},
    "EN": {"title": "🛡️ TikTok PRO Global", "step1": "📥 1. Paste Links", "step2": "📋 2. Ready", "start": "🚀 START", "ready": "Ready", "dl": "DOWNLOAD", "support": "Support this project"},
    "UA": {"title": "🛡️ TikTok PRO Україна", "step1": "📥 1. Вставте посилання", "step2": "📋 2. Готово", "start": "🚀 СТАРТ", "ready": "Готово", "dl": "ЗАВАНТАЖИТИ", "support": "Підтримати проект"},
    "RU": {"title": "🛡️ TikTok PRO Россия", "step1": "📥 1. Вставьте ссылки", "step2": "📋 2. Готово", "start": "🚀 СТАРТ", "ready": "Готово", "dl": "СКАЧАТЬ", "support": "Поддержать проект"}
}

t = translations[lang]

st.title(t["title"])

if 'links' not in st.session_state:
    st.session_state.links = []

col_in, col_out = st.columns([1, 1])

with col_in:
    st.subheader(t["step1"])
    urls_input = st.text_area("URLs:", height=250, placeholder="https://...")
    if st.button(t["start"]):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            results = []
            bar = st.progress(0)
            for i, url in enumerate(urls):
                try:
                    r = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                    if r.get('code') == 0: results.append(r['data']['play'])
                    time.sleep(0.3)
                except: pass
                bar.progress((i + 1) / len(urls))
            st.session_state.links = results

with col_out:
    st.subheader(t["step2"])
    if st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            js = f"""
            <body style="background:transparent; display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#28a745; font-weight:bold; font-family:sans-serif;">#{i+1} {t['ready']}</span>
                <button onclick="dl()" style="background:#28a745; color:white; border:none; border-radius:6px; padding:6px 15px; cursor:pointer;">{t['dl']}</button>
                <script>function dl() {{ fetch('{link}').then(r => r.blob()).then(b => {{ const u = window.URL.createObjectURL(b); const a = document.createElement('a'); a.href = u; a.download = "video_{i+1}.mp4"; a.click(); }}); }}</script>
            </body>
            """
            st.components.v1.html(js, height=45)

# SEKCJA "BUY ME A COFFEE" NA SAMYM DOLE
st.markdown(f"""
    <div class="coffee-container">
        <p style="color: #888;">{t['support']}</p>
        <a href="https://www.buymeacoffee.com/TWOJA_NAZWA" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px !important; width: 180px !important;" >
        </a>
    </div>
    """, unsafe_allow_html=True)
