import streamlit as st
import requests
import time

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

    /* Niebieski przycisk startowy */
    .stButton>button { 
        background: linear-gradient(145deg, #00d4ff, #0055ff); 
        color: white !important; font-weight: bold; border-radius: 30px; 
        height: 3.5em; width: 100%; border: none; font-size: 16px;
    }

    /* Karta wiersza - teraz całkowicie przezroczysta */
    .video-row {
        padding: 5px 0px;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: transparent;
    }

    /* NAPRAWA: Zielony tekst zamiast białych prostokątów */
    .video-info-green {
        color: #28a745 !important;
        font-size: 14px;
        font-weight: bold;
        background: none !important; /* Usuwa białe tło */
        border: none !important;
    }

    /* Zielony przycisk pobierania - wyraźny tekst */
    .dl-btn {
        background-color: #28a745 !important;
        color: white !important;
        padding: 6px 15px;
        text-decoration: none;
        border-radius: 6px;
        font-weight: bold;
        font-size: 13px;
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
            # Zwiększyłem wysokość, żeby przyciski się nie ucinały
            st.components.v1.html(js_code, height=50)
    else:
        st.write("Czekam na kliknięcie START...")
