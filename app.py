import streamlit as st
import requests
import time

st.set_page_config(page_title="TikTok PRO - Fast Download", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c22 0%, #000000 100%); color: white; }
    header, footer {visibility: hidden;}
    
    /* Mniejsze przyciski generowania */
    .stButton>button { 
        background: linear-gradient(145deg, #00d4ff, #0055ff); 
        color: white; font-weight: bold; border-radius: 50px; 
        height: 3em; width: 100%; font-size: 14px;
    }
    
    /* Styl kart i mniejszych przycisków pobierania */
    .download-card {
        background: rgba(20, 22, 28, 0.8); border: 1px solid #2a2d35;
        padding: 10px; border-radius: 12px; margin-bottom: 8px; text-align: center;
    }
    
    .fast-btn {
        background-color: #28a745; color: white !important;
        padding: 8px 20px; text-decoration: none; border-radius: 8px;
        font-weight: bold; display: inline-block; width: auto; 
        font-size: 14px; /* DWA RAZY MNIEJSZE NAPISY */
        cursor: pointer; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

if 'links' not in st.session_state:
    st.session_state.links = []

st.title("⚡ TikTok PRO - Szybkie Pobieranie")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("1. Wklej linki")
    urls_input = st.text_area("Lista:", height=300, placeholder="Linki jeden pod drugim...")
    if st.button("PRZYGOTUJ FILMY"):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            found = []
            bar = st.progress(0)
            for i, url in enumerate(urls):
                try:
                    res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                    if res.get('code') == 0:
                        found.append(res['data']['play'])
                    time.sleep(0.3)
                except: pass
                bar.progress((i+1)/len(urls))
            st.session_state.links = found

with col2:
    st.subheader("2. Pobierz pliki")
    if st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            # MECHANIZM JS DO POBIERANIA BEZ OTWIERANIA NOWEJ KARTY
            download_func = f"""
            <script>
            function download_{i}() {{
                fetch('{link}')
                    .then(resp => resp.blob())
                    .then(blob => {{
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = url;
                        a.download = 'video_{i+1}.mp4';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    }})
                    .catch(() => window.open('{link}', '_blank'));
            }}
            </script>
            <div class="download-card">
                <span style="font-size: 12px; color: #888;">Film #{i+1}</span><br>
                <button onclick="download_{i}()" class="fast-btn">ZAPISZ TERAZ</button>
            </div>
            """
            st.components.v1.html(download_func, height=80)
            
        if st.sidebar.button("Wyczyść wszystko"):
            st.session_state.links = []
            st.rerun()

st.info("💡 Napisy są teraz mniejsze. Jeśli nadal otwiera stronę zamiast pobierać, upewnij się, że Chrome nie blokuje pobierania plików z wielu źródeł.")
