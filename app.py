import streamlit as st
import requests
import time

st.set_page_config(page_title="TikTok PRO - Fast Download", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c22 0%, #000000 100%); color: white; }
    header, footer {visibility: hidden;}
    .stButton>button { 
        background: linear-gradient(145deg, #00d4ff, #0055ff); 
        color: white; font-weight: bold; border-radius: 50px; height: 3.5em; width: 100%;
    }
    .download-card {
        background: #0a0a0a; border: 1px solid #00d4ff;
        padding: 15px; border-radius: 15px; margin-bottom: 10px; text-align: center;
    }
    .fast-btn {
        background-color: #28a745; color: white !important;
        padding: 15px 40px; text-decoration: none; border-radius: 10px;
        font-weight: bold; display: block; width: 100%; font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'links' not in st.session_state:
    st.session_state.links = []

st.title("⚡ TikTok PRO - Szybkie Pobieranie")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Wklej linki")
    urls_input = st.text_area("Lista:", height=300)
    if st.button("PRZYGOTUJ FILMY"):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            found = []
            for url in urls:
                try:
                    res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                    if res.get('code') == 0:
                        found.append(res['data']['play'])
                    time.sleep(0.3)
                except: pass
            st.session_state.links = found

with col2:
    st.subheader("2. Pobierz jednym kliknięciem")
    if st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            # Tutaj jest klucz: Atrybut download i brak target="_blank"
            st.markdown(f"""
                <div class="download-card">
                    <p>Film #{i+1}</p>
                    <a href="{link}" download="video_{i+1}.mp4" class="fast-btn">
                        ⬇️ ZAPISZ TERAZ
                    </a>
                </div>
            """, unsafe_allow_html=True)
            
        if st.button("Wyczyść listę"):
            st.session_state.links = []
            st.rerun()

st.info("💡 PRO TIP: W ustawieniach Chrome wyłącz 'Pytaj, gdzie zapisać każdy plik przed pobraniem'. Wtedy każde kliknięcie w zielony przycisk to natychmiastowy zapis!")
