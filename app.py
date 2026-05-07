import streamlit as st
import requests
import time

# Konfiguracja strony
st.set_page_config(page_title="TikTok PRO - Black Edition", layout="wide")

# STYLIZACJA (Tło jak w logo)
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle, #1a1c22 0%, #000000 100%);
        color: #ffffff; 
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stTextArea textarea { 
        background-color: #050505; 
        color: #00d4ff; 
        border: 2px solid #00d4ff; 
        border-radius: 12px;
    }
    .stButton>button { 
        background: linear-gradient(145deg, #00d4ff, #0055ff); 
        color: white; 
        font-weight: bold; 
        border: none; 
        border-radius: 50px; 
        height: 3.8em; 
        width: 100%; 
        box-shadow: 0 4px 15px rgba(0, 85, 255, 0.4);
        text-transform: uppercase;
    }
    .video-card { 
        border: 1px solid #2a2d35; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 15px; 
        background: rgba(20, 22, 28, 0.8); 
        text-align: center;
    }
    .download-btn {
        background: #28a745;
        color: white !important;
        padding: 12px 30px;
        text-decoration: none;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# INICJALIZACJA PAMIĘCI (Session State)
if 'links' not in st.session_state:
    st.session_state.links = []

st.title("🛡️ TikTok PRO - Masowe Pobieranie")

col_input, col_output = st.columns([1, 2])

with col_input:
    st.subheader("📥 1. Wklej linki")
    urls_input = st.text_area("Lista linków:", height=400, placeholder="Wklej linki jeden pod drugim...")
    
    if st.button("GENERUJ LISTĘ DO POBRANIA"):
        if urls_input:
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            temp_links = []
            
            with st.spinner('Przetwarzanie...'):
                for index, url in enumerate(urls):
                    try:
                        api_url = f"https://www.tikwm.com/api/?url={url}"
                        res = requests.get(api_url).json()
                        if res.get('code') == 0:
                            video_url = res.get('data').get('play')
                            temp_links.append(video_url)
                        time.sleep(0.5)
                    except:
                        st.error(f"Błąd przy linku nr {index+1}")
            
            st.session_state.links = temp_links # Zapisujemy do pamięci sesji
        else:
            st.warning("Pole jest puste!")

with col_output:
    st.subheader("📋 2. Twoje Pliki")
    
    # Wyświetlamy linki z pamięci sesji (dzięki temu nie znikną)
    if st.session_state.links:
        for i, link in enumerate(st.session_state.links):
            st.markdown(f"""
                <div class='video-card'>
                    <span style='color: #00d4ff;'>GOTOWY DO POBRANIA #{i+1}</span><br>
                    <a href="{link}" target="_blank" class="download-btn">⬇️ POBIERZ PLIK</a>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        if st.button("🚀 URUCHOM AUTOMATYCZNE POBIERANIE WSZYSTKIEGO"):
            # Skrypt JS do masowego otwierania okien
            js_code = f"""
            <script>
            const links = {st.session_state.links};
            links.forEach((link, i) => {{
                setTimeout(() => {{
                    const win = window.open(link, '_blank');
                    if(!win) {{
                        alert('Zablokowano okno! Zezwól na wyskakujące okienka w przeglądarce.');
                    }}
                }}, i * 1500);
            }});
            </script>
            """
            st.components.v1.html(js_code, height=0)
            st.info("Pobieranie powinno zacząć się za chwilę. Upewnij się, że przeglądarka nie zablokowała wyskakujących okienek!")

# Przycisk do czyszczenia listy
if st.sidebar.button("Wyczyść wszystko"):
    st.session_state.links = []
    st.rerun()
