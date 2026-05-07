import streamlit as st
import requests
import time

# Konfiguracja strony
st.set_page_config(page_title="TikTok PRO - Black Edition", layout="wide")

# STYLIZACJA POD TWOJE LOGO
st.markdown("""
    <style>
    /* Tło identyczne jak na Twoim logo (ciemny gradient) */
    .stApp { 
        background: radial-gradient(circle, #1a1c22 0%, #000000 100%);
        color: #ffffff; 
    }
    
    /* Ukrycie elementów Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Neonowe pole tekstowe */
    .stTextArea textarea { 
        background-color: #050505; 
        color: #00d4ff; 
        border: 2px solid #00d4ff; 
        border-radius: 12px;
        box-shadow: inset 0 0 10px rgba(0, 212, 255, 0.2);
    }
    
    /* Przycisk pasujący do tarczy logo */
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
        letter-spacing: 1px;
    }
    
    /* Karty z filmami w kolorze tarczy logo */
    .video-card { 
        border: 1px solid #2a2d35; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 15px; 
        background: rgba(20, 22, 28, 0.8); 
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
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
        box-shadow: 0 4px 10px rgba(40, 167, 69, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ TikTok PRO - Masowe Pobieranie")

col_input, col_output = st.columns([1, 2])

with col_input:
    st.subheader("📥 1. Wklej linki")
    urls_input = st.text_area("Lista linków:", height=400, placeholder="Wklej tutaj listę filmów...")
    process_btn = st.button("GENERUJ LISTĘ DO POBRANIA")

with col_output:
    st.subheader("📋 2. Twoje Pliki")
    if process_btn and urls_input:
        urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
        links_for_js = []
        
        for index, url in enumerate(urls):
            try:
                api_url = f"https://www.tikwm.com/api/?url={url}"
                res = requests.get(api_url).json()
                
                if res.get('code') == 0:
                    video_url = res.get('data').get('play')
                    links_for_js.append(video_url)
                    
                    st.markdown(f"""
                        <div class='video-card'>
                            <span style='color: #00d4ff; font-size: 0.9em;'>GOTOWY DO POBRANIA #{index+1}</span><br>
                            <a href="{video_url}" download class="download-btn">⬇️ POBIERZ PLIK</a>
                        </div>
                    """, unsafe_allow_html=True)
                time.sleep(0.5)
            except:
                st.error(f"Błąd przy linku nr {index+1}")
        
        if links_for_js:
            st.divider()
            # Przycisk "wszystko na raz"
            if st.button("🚀 URUCHOM AUTOMATYCZNE POBIERANIE WSZYSTKIEGO"):
                # Ten skrypt "klika" za Ciebie w linki co 1.5 sekundy
                js_code = f"""
                <script>
                const links = {links_for_js};
                links.forEach((link, i) => {{
                    setTimeout(() => {{
                        const a = document.createElement('a');
                        a.href = link;
                        a.target = '_blank';
                        a.download = 'video_' + i + '.mp4';
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                    }}, i * 1500);
                }});
                </script>
                """
                st.components.v1.html(js_code, height=0)
                st.warning("Jeśli nic się nie dzieje, kliknij w ikonkę blokady okienek w pasku adresu przeglądarki i wybierz 'Zezwalaj'!")

    elif process_btn:
        st.warning("Pole z linkami jest puste!")
