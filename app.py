import streamlit as st
import requests
import time

st.set_page_config(page_title="TikTok PRO - Hurtowe Pobieranie", layout="wide")

# Nowy styl - jeszcze bardziej profesjonalny
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextArea textarea { background-color: #1a1c24; color: #00d4ff; border: 1px solid #00d4ff; border-radius: 10px; }
    .stButton>button { background: linear-gradient(90deg, #00d4ff, #0055ff); color: white; font-weight: bold; border: none; border-radius: 10px; height: 3.5em; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00d4ff; }
    .video-card { border: 1px solid #333; padding: 15px; border-radius: 15px; margin-bottom: 20px; background: #161b22; text-align: center; }
    .download-link { background-color: #28a745; color: white !important; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 TikTok PRO - Auto-Downloader")

col_input, col_output = st.columns([1, 2])

with col_input:
    st.subheader("📥 1. Lista linków")
    urls_input = st.text_area("Wklej linki (jeden pod drugim):", height=400, placeholder="https://www.tiktok.com/...")
    process_btn = st.button("PRZETWÓRZ I PZYGOTUJ DO POBRANIA")

with col_output:
    st.subheader("📋 2. Gotowe do zapisu")
    if process_btn and urls_input:
        urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
        
        all_download_links = []
        
        for index, url in enumerate(urls):
            try:
                api_url = f"https://www.tikwm.com/api/?url={url}"
                res = requests.get(api_url).json()
                
                if res.get('code') == 0:
                    data = res.get('data')
                    video_url = data.get('play')
                    title = data.get('title', f'Film {index+1}')[:50]
                    
                    all_download_links.append(video_url)
                    
                    st.markdown(f"""
                        <div class='video-card'>
                            <p style='color: #00d4ff;'><b>{index+1}. {title}...</b></p>
                            <a href="{video_url}" download="tiktok_video_{index+1}.mp4" target="_blank" class="download-link">
                                ✅ KLIKNIJ ABY ZPISAĆ NA DYSKU
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Film {index+1}: TikTok zablokował link.")
                
                time.sleep(1) # Szybka przerwa
                
            except Exception as e:
                st.error(f"⚠️ Problem przy nr {index+1}")
        
        if all_download_links:
            st.divider()
            st.balloons()
            st.success(f"Przygotowano {len(all_download_links)} filmów!")
            st.info("Podpowiedź: W ustawieniach Chrome możesz wyłączyć 'Pytaj, gdzie zapisać każdy plik', wtedy pobieranie pójdzie błyskawicznie!")

    elif process_btn:
        st.warning("Brak linków!")
