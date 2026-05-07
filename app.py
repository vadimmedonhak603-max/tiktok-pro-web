import streamlit as st
import requests
import time

# Konfiguracja PRO
st.set_page_config(page_title="TikTok PRO Global", layout="wide")

# SŁOWNIK TŁUMACZEŃ
translations = {
    "PL": {
        "title": "🛡️ TikTok PRO Downloader",
        "step1": "📥 1. Wklej Linki",
        "step2": "📋 2. Gotowe",
        "start": "🚀 START / PRZETWÓRZ",
        "ready": "Gotowe",
        "download": "POBIERZ",
        "clear": "Wyczyść wszystko",
        "wait": "Czekam na linki...",
        "placeholder": "Wklej linki tutaj..."
    },
    "EN": {
        "title": "🛡️ TikTok PRO Global",
        "step1": "📥 1. Paste Links",
        "step2": "📋 2. Ready",
        "start": "🚀 START / PROCESS",
        "ready": "Ready",
        "download": "DOWNLOAD",
        "clear": "Clear all",
        "wait": "Waiting for links...",
        "placeholder": "Paste links here..."
    },
    "RU": {
        "title": "🛡️ TikTok PRO Россия",
        "step1": "📥 1. Вставьте ссылки",
        "step2": "📋 2. Готово",
        "start": "🚀 СТАРТ / ОБРАБОТАТЬ",
        "ready": "Готово",
        "download": "СКАЧАТЬ",
        "clear": "Очистить всё",
        "wait": "Жду ссылки...",
        "placeholder": "Вставьте ссылки сюда..."
    }
}

# WYBÓR JĘZYKA W SIDEBARZE
st.sidebar.title("Settings / Ustawienia")
lang_choice = st.sidebar.selectbox("Language / Język / Язык", ["PL", "EN", "RU"])
t = translations[lang_choice]

# Stylizacja (Twoje ulubione kolory)
st.markdown(f"""
    <style>
    .stApp {{ background: radial-gradient(circle, #1a1c22 0%, #000000 100%); color: white; }}
    header, footer {{visibility: hidden;}}
    .stTextArea textarea {{ background-color: #050505 !important; color: #00d4ff !important; border: 1px solid #00d4ff !important; border-radius: 12px; }}
    .stButton>button {{ background: linear-gradient(145deg, #00d4ff, #0055ff) !important; color: white !important; font-weight: bold; border-radius: 30px; height: 3.5em; width: 100%; border: none; font-size: 16px; }}
    iframe {{ background-color: transparent !important; border: none !important; }}
    </style>
    """, unsafe_allow_html=True)

if 'links' not in st.session_state:
    st.session_state.links = []

st.title(t["title"])

col_in, col_out = st.columns([1, 1])

with col_in:
    st.subheader(t["step1"])
    urls_input = st.text_area("URLs:", height=300, placeholder=t["placeholder"])
    
    if st.button(t["start"]):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            results = []
            bar = st.progress(0)
            for i, url in enumerate(urls):
                try:
                    r = requests.get(f"https://www.tikwm.com/api/?url={{url}}").json()
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
            js_code = f'''
            <body style="background-color: transparent; margin: 0; padding: 0; display: flex; justify-content: space-between; align-items: center; overflow: hidden;">
                <span style="color: #28a745 !important; font-weight: bold; font-family: sans-serif; font-size: 14px;">Video #{i+1} {t["ready"]}</span>
                <button onclick="dl()" style="background-color: #28a745; color: white; border: none; border-radius: 6px; padding: 6px 15px; font-weight: bold; cursor: pointer; font-size: 12px;">{t["download"]}</button>
                <script>function dl() {{ fetch('{link}').then(r => r.blob()).then(b => {{ const u = window.URL.createObjectURL(b); const a = document.createElement('a'); a.href = u; a.download = "video_{i+1}.mp4"; document.body.appendChild(a); a.click(); document.body.removeChild(a); window.URL.revokeObjectURL(u); }}); }}</script>
            </body>
            '''
            st.components.v1.html(js_code, height=45)
    else:
        st.write(t["wait"])

if st.sidebar.button(t["clear"]):
    st.session_state.links = []
    st.rerun()
