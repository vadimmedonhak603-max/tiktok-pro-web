import streamlit as st
import requests
import time

# Konfiguracja PRO - czarna elegancja
st.set_page_config(page_title="TikTok PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle, #1a1c22 0%, #000000 100%); 
        color: white; 
    }
    header, footer {visibility: hidden;}
    
    /* Pole tekstowe */
    .stTextArea textarea { 
        background-color: #050505; color: #00d4ff; 
        border: 1px solid #00d4ff; border-radius: 12px;
    }

    /* NIEBIESKI PRZYCISK STARTOWY */
    .stButton>button { 
        background: linear-gradient(145deg, #00d4ff, #0055ff); 
        color: white; font-weight: bold; border-radius: 30px; 
        height: 3.5em; width: 100%; border: none; font-size: 16px;
        box-shadow: 0 4px 15px rgba(0, 85, 255, 0.3);
    }

    /* Karta wiersza - mniejsza */
    .video-row {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #2a2d35;
        padding: 5px 15px;
        border-radius: 8px;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* ZIELONE NAPISY (tam gdzie pokazałeś palcem) */
    .video-info-green {
        color: #28a745 !important;
        font-size: 13px;
        font-weight: bold;
    }

    /* Mały zielony przycisk pobierania */
    .dl-btn {
        background-color: #28a745;
        color: white !important;
        padding: 4px 12px;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
        font-size: 12px;
        border: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

if 'links' not in st.session_state:
    st.session_state.links = []

st.title("🛡️ TikTok PRO Downloader")

col_in, col_out = st.columns([1, 1])

with col_in:
    st.subheader("📥 1. Paste Links / Wklej Linki")
    urls_input = st.text_area("URLs:", height=300, placeholder="Paste links here...")
    
    # PRZYRÓCONY NIEBIESKI PRZYCISK
    if st.button("🚀 START / PRZETWÓRZ"):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            results = []
            bar = st.progress(0)
            for i, url in enumerate(urls):
                try:
                    r = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                    if r.get('code') == 0:
                        results.append(r['data']['play'])
                    time.sleep(0.3)
                except: pass
                bar.progress((i + 1) / len(urls))
            st.session_state.links = results

with col_out:
    st.subheader("📋 2. Ready / Gotowe")
    if st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            js_code = f"""
            <script>
            function forceDl_{i}() {{
                fetch('{link}')
                .then(r => r.blob())
                .then(b => {{
                    const u = window.URL.createObjectURL(b);
                    const a = document.createElement('a');
                    a.href = u;
                    a.download = "video_{i+1}.mp4";
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(u);
                }});
            }}
            </script>
            <div class="video-row">
                <span class="video-info-green">Video #{i+1} Ready / Gotowe</span>
                <button onclick="forceDl_{i}()" class="dl-btn">DOWNLOAD / POBIERZ</button>
            </div>
            """
            st.components.v1.html(js_code, height=45)
    else:
        st.write("Czekam na kliknięcie START... / Waiting for START...")

if st.sidebar.button("Wyczyść / Clear"):
    st.session_state.links = []
    st.rerun()
