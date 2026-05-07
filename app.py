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

st.title("🚀 TikTok PRO - Masowy Downloader v2")

# Podział na dwie kolumny (Paski)
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
            with st.container():
                try:
                    # Używamy silnika Cobalt - obecnie najlepszy na blokady
                    headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "url": url,
                        "videoQuality": "1080",
                        "filenameStyle": "classic"
                    }
                    
                    # Wysyłamy prośbę do instancji Cobalt
                    api_res = requests.post("https://api.cobalt.tools/api/json", json=data, headers=headers)
                    res_data = api_res.json()
                    
                    if res_data.get('status') == 'stream':
                        video_url = res_data.get('url')
                        st.markdown(f"<div class='video-card'>", unsafe_allow_html=True)
                        st.success(f"Film {index+1} gotowy!")
                        st.video(video_url)
                        st.markdown(f"[📥 POBIERZ TEN FILM]({video_url})")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Film {index+1}: TikTok na razie blokuje ten link. Spróbuj za chwilę.")
                    
                    # Mała przerwa, żeby TikTok nas nie uznał za robota
                    time.sleep(1.5)
                    
                except Exception as e:
                    st.error(f"⚠️ Problem z połączeniem przy filmie {index+1}")
    elif process_btn:
        st.warning("Lista linków jest pusta!")
