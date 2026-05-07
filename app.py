import streamlit as st
import requests
import time

st.set_page_config(page_title="TikTok PRO", layout="wide")

# WYBÓR JĘZYKA - Od razu na górze
lang = st.sidebar.radio("Language / Язык", ["English", "Русский"])

# Słownik
if lang == "English":
    text = {"h1": "TikTok PRO Downloader", "btn": "START / PROCESS", "ready": "Ready", "dl": "DOWNLOAD"}
else:
    text = {"h1": "TikTok PRO Загрузчик", "btn": "СТАРТ / ОБРАБОТАТЬ", "ready": "Готово", "dl": "СКАЧАТЬ"}

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c22 0%, #000000 100%); color: white; }
    header, footer {visibility: hidden;}
    .stTextArea textarea { background-color: #050505 !important; color: #00d4ff !important; border: 1px solid #00d4ff !important; }
    .stButton>button { background: linear-gradient(145deg, #00d4ff, #0055ff) !important; color: white !important; font-weight: bold; border-radius: 30px; height: 3.5em; width: 100%; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title(f"🛡️ {text['h1']}")

col1, col2 = st.columns([1, 1])

with col1:
    urls_input = st.text_area("URLs:", height=300, placeholder="Paste links here...")
    if st.button(text['btn']):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            results = []
            for url in urls:
                try:
                    r = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                    if r.get('code') == 0: results.append(r['data']['play'])
                except: pass
            st.session_state.links = results

with col2:
    if 'links' in st.session_state and st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            js = f"""
            <body style="background:transparent; display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#28a745; font-weight:bold; font-family:sans-serif;">#{i+1} {text['ready']}</span>
                <button onclick="dl()" style="background:#28a745; color:white; border:none; border-radius:6px; padding:6px 15px; cursor:pointer;">{text['dl']}</button>
                <script>function dl() {{ fetch('{link}').then(r => r.blob()).then(b => {{ const u = window.URL.createObjectURL(b); const a = document.createElement('a'); a.href = u; a.download = "video_{i+1}.mp4"; a.click(); }}); }}</script>
            </body>
            """
            st.components.v1.html(js, height=45)
