import streamlit as st
import requests

st.set_page_config(page_title="TikTok PRO - Hurtowe Pobieranie", layout="wide")

# Stylizacja tła i napisów
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #00d4ff; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 TikTok PRO - Masowy Downloader")

# Dwa paski (kolumny), o które prosiłeś
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Wklej linki")
    urls_input = st.text_area("Wklej listę linków z TikToka (jeden pod drugim):", height=300, placeholder="https://www.tiktok.com/@user/video/...\nhttps://www.tiktok.com/@user/video/...")

with col2:
    st.subheader("📋 Status pobierania")
    if st.button("URUCHOM POBIERANIE MASOWE"):
        if urls_input:
            urls = urls_input.split('\n')
            urls = [u.strip() for u in urls if u.strip()]
            
            for index, url in enumerate(urls):
                try:
                    # Używamy zewnętrznego API, które omija błąd 403
                    api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
                    response = requests.get(api_url).json()
                    
                    video_data = response.get('video', {})
                    no_watermark = video_data.get('noWatermark') or video_data.get('noWatermark2')
                    
                    if no_watermark:
                        st.success(f"✅ Film {index+1} gotowy!")
                        st.video(no_watermark)
                        st.markdown(f"[📥 POBIERZ FILM {index+1} BEZ ZNAKU]({no_watermark})")
                    else:
                        st.error(f"❌ Nie udało się pobrać filmu {index+1}")
                except Exception as e:
                    st.error(f"⚠️ Błąd przy linku {index+1}. TikTok zablokował połączenie.")
        else:
            st.warning("Wklej chociaż jeden link!")
