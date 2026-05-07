import streamlit as st
import requests
import time

st.set_page_config(page_title="TikTok PRO", layout="wide")

# Stylizacja Globalna
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle, #1a1c22 0%, #000000 100%); 
        color: white; 
    }
    header, footer {visibility: hidden;}
    
    /* Naprawa pól tekstowych */
    .stTextArea textarea { 
        background-color: #050505 !important; color: #00d4ff !important; 
        border: 1px solid #00d4ff !important; border-radius: 12px;
    }

    /* Niebieski przycisk startowy */
    .stButton>button { 
        background: linear-gradient(145deg, #00d4ff, #0055ff) !important; 
        color: white !important; font-weight: bold; border-radius: 30px; 
        height: 3.5em; width: 100%; border: none;
    }

    /* USUNIĘCIE BIAŁYCH RAMER Z KOMPONENTÓW HTML */
    iframe {
        background-color: transparent !important;
        border: none !important;
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
            # Wymuszamy kolory bezpośrednio wewnątrz HTML
            js_code = f"""
            <html>
            <body style="background-color: transparent; margin: 0; padding: 0; font-family: sans-serif; display: flex; justify-content: space-between; align-items: center; overflow: hidden;">
                <span style="color: #28a745 !important; font-weight: bold; font-size: 14px;">
                    Video #{i+1} Ready / Gotowe
                </span>
                <button onclick="forceDl()" style="background-color: #28a745; color: white; border: none; border-radius: 6px; padding: 6px 15px; font-weight: bold; cursor: pointer; font-size: 12px;">
                    DOWNLOAD / POBIERZ
                </button>

                <script>
                function forceDl() {{
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
            </body>
            </html>
            """
            st.components.v1.html(js_code, height=45)
    else:
        st.write("Czekam na kliknięcie START...")
