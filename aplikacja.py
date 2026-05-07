import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="TikTok PRO - Hurtowe Pobieranie", layout="centered")

st.markdown("<h1 style='text-align: center; color: #00d4ff;'>TikTok PRO - Batch Downloader</h1>", unsafe_allow_html=True)

# Duże pole na wiele linków
urls_input = st.text_area("Wklej listę linków z TikToka (jeden pod drugim):", height=200)

if st.button("POBIERZ WSZYSTKIE FILMY"):
    if urls_input:
        urls = urls_input.split('\n')
        urls = [u.strip() for u in urls if u.strip()]
        
        st.info(f"Znaleziono {len(urls)} linków. Zaczynam pobieranie...")
        
        for index, url in enumerate(urls):
            try:
                st.write(f"🔄 Pobieranie filmu nr {index+1}...")
                
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'noplaylist': True,
                    'quiet': True,
                    # To pomaga uniknąć błędu 403 (udajemy przeglądarkę):
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_url = info['url']
                    title = info.get('title', f'video_{index}')
                    
                    st.video(video_url)
                    st.success(f"Gotowe: {title}")
                    st.markdown(f"[KLIKNIJ TUTAJ ABY ZAPISAĆ FILM {index+1}]({video_url})")
                    st.divider()
                    
            except Exception as e:
                st.error(f"Błąd przy linku nr {index+1}: Link jest niepoprawny lub TikTok go zablokował.")
    else:
        st.warning("Najpierw wklej linki!")