import streamlit as st
import requests
import time

st.set_page_config(page_title="TikTok PRO - Hurtowe Pobieranie", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextArea textarea { background-color: #1a1c24; color: #00d4ff; border: 1px solid #00d4ff; }
    .stButton>button { background: linear-gradient(90deg, #00d4ff, #0055ff); color: white; font-weight: bold; border: none; border-radius: 10px; height: 3em; }
    .video-card { border: 1px solid #333; padding: 10px; border-radius: 10px; margin-bottom: 20px; background: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 TikTok PRO - Masowy Downloader")

col_input, col_output = st.columns([1, 2])

with col_input:
    st.subheader("📥 1. Wklej linki")
    urls_input = st.text_area("Wklej listę linków (jeden pod drugim):", height=400, placeholder="https://www.tiktok.com/...")
    process_btn = st.button("URUCHOM POBIERANIE MASOWE")

with col_output:
    st.subheader("📋 2. Twoje Filmy")
    if process_btn and urls_input:
        urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
        
        for index, url in enumerate(urls):
            try:
                # Silnik TikWM - stabilniejszy niż Cobalt
                api_url = f"https://www.tikwm.com/api/?url={url}"
                res = requests.get(api_url).json()
                
                if res.get('code') == 0:
                    data = res.get('data')
                    video_url = data.get('play')
                    title = data.get('title', f'Film {index+1}')
                    
                    st.markdown(f"<div class='video-card'>", unsafe_allow_html=True)
                    st.success(f"✅ {title}")
                    st.video(video_url)
                    st.markdown(f"[📥 POBIERZ TEN FILM]({video_url})")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Film {index+1}: TikTok zablokował to zapytanie.")
                
                time.sleep(2) # Przerwa, żeby nie dostać bana
                
            except Exception as e:
                st.error(f"⚠️ Problem techniczny przy filmie {index+1}")
    elif process_btn:
        st.warning("Lista linków jest pusta!")
    
