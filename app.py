import streamlit as st
import requests
import time

# Ustawienia wyglądu - Ciemny gradient z Twojego logo
st.set_page_config(page_title="TikTok PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c22 0%, #000000 100%); color: white; }
    header, footer {visibility: hidden;}
    
    /* Napisy i pola */
    h1, h2, h3, p { font-family: 'Segoe UI', sans-serif; }
    .stTextArea textarea { 
        background-color: #050505; color: #00d4ff; 
        border: 1px solid #00d4ff; border-radius: 10px;
    }

    /* Przyciski główne */
    .stButton>button { 
        background: linear-gradient(145deg, #00d4ff, #0055ff); 
        color: white; font-weight: bold; border-radius: 30px; 
        height: 3em; width: 100%; border: none; font-size: 14px;
    }

    /* Karty pobierania - mniejsze i dyskretne */
    .video-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #2a2d35;
        padding: 8px 15px;
        border-radius: 10px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .dl-btn {
        background-color: #28a745;
        color: white !important;
        padding: 5px 15px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px; /* Mały, czytelny napis */
        border: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

if 'links' not in st.session_state:
    st.session_state.links = []

st.title("🛡️ TikTok PRO Downloader")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 1. Paste Links / Wklej Linki")
    input_data = st.text_area("URLs:", height=300, placeholder="Paste TikTok links here...")
    if st.button("PROCESS / PRZETWÓRZ"):
        if input_data:
            urls = [u.strip() for u in input_data.split('\n') if u.strip()]
            results = []
            progress = st.progress(0)
            for i, url in enumerate(urls):
                try:
                    r = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                    if r.get('code') == 0:
                        results.append(r['data']['play'])
                    time.sleep(0.3)
                except: pass
                progress.progress((i + 1) / len(urls))
            st.session_state.links = results

with col2:
    st.subheader("📋 2. Ready / Gotowe")
    if st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            # Skrypt wymuszający pobranie pliku na dysk
            js_download = f"""
            <script>
            function startDownload_{i}() {{
                fetch('{link}')
                .then(response => response.blob())
                .then(blob => {{
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = "video_{i+1}.mp4";
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                }})
                .catch(() => window.open('{link}', '_blank'));
            }}
            </script>
            <div class="video-item">
                <span style="color: #00d4ff; font-size: 13px;">Video #{i+1}</span>
                <button onclick="startDownload_{i}()" class="dl-btn">DOWNLOAD / POBIERZ</button>
            </div>
            """
            st.components.v1.html(js_download, height=55)
        
        if st.sidebar.button("Clear / Wyczyść"):
            st.session_state.links = []
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("Tip: If the file opens in a new tab, right-click 'Save as'.")
