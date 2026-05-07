import streamlit as st
import subprocess
import os

# Konfiguracja wyglądu strony (pasująca do Twojego czarnego stylu)
st.set_page_config(page_title="TikTok PRO Downloader", page_icon="🚀", layout="centered")

# Stylizacja CSS dla zachowania estetyki PRO
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #00f2ff; color: black; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #1a1c24; color: white; }
    h1 { color: #00f2ff; text-align: center; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("TikTok PRO Online 🎬")
st.write("Wklej link poniżej, aby pobrać wideo bez znaku wodnego.")

# Pole wejściowe dla użytkownika
url = st.text_input("Link do TikToka:", placeholder="https://www.tiktok.com/@user/video/...")

if st.button("POBIERZ WIDEO"):
    if url:
        with st.spinner('Przetwarzanie... to może chwilę potrwać.'):
            try:
                # Używamy yt-dlp do pobrania filmu do pamięci tymczasowej
                # --get-url wyciąga bezpośredni link do pliku wideo bez pobierania go na serwer
                command = [
                    'yt-dlp',
                    '--extractor-args', 'tiktok:api_hostname=api16-normal-c-useast1a.tiktokv.com;app_name=musical_ly',
                    '-g', # Zwróć tylko bezpośredni adres URL filmu
                    url
                ]
                
                direct_url = subprocess.check_output(command).decode('utf-8').strip()
                
                st.success("Gotowe! Kliknij poniżej, aby zapisać film:")
                # Przycisk prowadzący bezpośrednio do pliku
                st.video(direct_url)
                st.markdown(f'<a href="{direct_url}" download="video.mp4" style="text-decoration:none;"><div style="background-color:#00FF7F;color:black;padding:10px;text-align:center;border-radius:5px;font-weight:bold;">ZAPISZ NA DYSKU</div></a>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Wystąpił błąd. Upewnij się, że link jest poprawny. Opis: {e}")
    else:
        st.warning("Najpierw wklej link!")

st.info("Created by TikTok PRO Team")