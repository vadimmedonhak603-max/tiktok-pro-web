import streamlit as st
import requests
import time

# 1. Konfiguracja i Stylizacja PRO
st.set_page_config(page_title="TikTok PRO - Black Edition", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle, #1a1c22 0%, #000000 100%);
        color: #ffffff; 
    }
    header, footer {visibility: hidden;}
    .stTextArea textarea { 
        background-color: #050505; color: #00d4ff; 
        border: 2px solid #00d4ff; border-radius: 12px;
    }
    .stButton>button { 
        background: linear-gradient(145deg, #00d4ff, #0055ff); 
        color: white; font-weight: bold; border: none; 
        border-radius: 50px; height: 3.8em; width: 100%; 
        box-shadow: 0 4px 15px rgba(0, 85, 255, 0.4);
    }
    .video-card { 
        border: 1px solid #2a2d35; padding: 20px; 
        border-radius: 15px; margin-bottom: 15px; 
        background: rgba(20, 22, 28, 0.8); text-align: center;
    }
    .download-btn {
        background: #28a745; color: white !important; 
        padding: 12px 30px; text-decoration: none; 
        border-radius: 50px; font-weight: bold; display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicjalizacja pamięci
if 'links' not in st.session_state:
    st.session_state.links = []

st.title("🛡️ TikTok PRO - Black Mass Downloader")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📥 Krok 1: Wklej linki")
    urls_input = st.text_area("Linki (jeden pod drugim):", height=350)
    
    if st.button("GENERUJ LISTĘ DO POBRANIA"):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            found_links = []
            bar = st.progress(0)
            for i, url in enumerate(urls):
                try:
                    api_res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                    if api_res.get('code') == 0:
                        found_links.append(api_res['data']['play'])
                    time.sleep(0.5)
                except:
                    st.error(f"Błąd przy linku {i+1}")
                bar.progress((i + 1) / len(urls))
            st.session_state.links = found_links
        else:
            st.warning("Wklej linki!")

with col_right:
    st.subheader("📋 Krok 2: Pobierz pliki")
    if st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            st.markdown(f"""
                <div class='video-card'>
                    <span style='color: #00d4ff;'>GOTOWY FILM #{i+1}</span><br><br>
                    <a href="{link}" target="_blank" class="download-btn">ZAPISZ PLIK MP4</a>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        if st.button("🚀 URUCHOM AUTOMATYCZNE POBIERANIE WSZYSTKIEGO"):
            js_code = f"""
            <script>
            const links = {st.session_state.links};
            links.forEach((link, i) => {{
                setTimeout(() => {{
                    const a = document.createElement('a');
                    a.href = link;
                    a.download = `tiktok_pro_${{i+1}}.mp4`;
                    a.target = '_blank';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                }}, i * 1500);
            }});
            </script>
            """
            st.components.v1.html(js_code, height=0)
            st.info("Pobieranie ruszyło! Pamiętaj o odblokowaniu 'wyskakujących okienek' w Chrome!")

if st.sidebar.button("Wyczyść pamięć"):
    st.session_state.links = []
    st.rerun()
