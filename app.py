import streamlit as st
import requests
import time

# Ustawienia strony - głęboka czerń
st.set_page_config(page_title="TikTok PRO - Black Edition", layout="wide")

st.markdown("""
    <style>
    /* Cała strona na czarno */
    .stApp { background-color: #000000; color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Czarny pasek tekstowy z neonową ramką */
    .stTextArea textarea { 
        background-color: #050505; 
        color: #00d4ff; 
        border: 2px solid #00d4ff; 
        border-radius: 10px;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Przycisk neonowy */
    .stButton>button { 
        background: linear-gradient(90deg, #00d4ff, #0055ff); 
        color: white; 
        font-weight: bold; 
        border: none; 
        border-radius: 30px; 
        height: 3.5em; 
        width: 100%; 
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    }
    
    /* Karty filmów - czarne */
    .video-card { 
        border: 1px solid #1a1a1a; 
        padding: 15px; 
        border-radius: 15px; 
        margin-bottom: 10px; 
        background: #0a0a0a; 
        text-align: center; 
    }
    
    .download-btn {
        background-color: #28a745;
        color: white !important;
        padding: 12px 25px;
        text-decoration: none;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-top: 5px;
        border: 1px solid #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 TikTok PRO - BLACK MASS DOWNLOAD")

col_input, col_output = st.columns([1, 2])

with col_input:
    st.subheader("📥 Lista linków")
    urls_input = st.text_area("Wklej linki jeden pod drugim:", height=450)
    process_btn = st.button("GENERUJ LINKI DO POBRANIA")

with col_output:
    st.subheader("📋 Gotowe pliki")
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
                            <span style='color: #888;'>Film #{index+1}</span><br>
                            <a href="{video_url}" download class="download-btn">⬇️ ZAPISZ TERAZ</a>
                        </div>
                    """, unsafe_allow_html=True)
                time.sleep(0.5)
            except:
                st.error(f"Błąd przy nr {index+1}")
        
        if links_for_js:
            st.success(f"Przygotowano {len(links_for_js)} filmów!")
            
            # MAGIA: Przycisk, który próbuje otworzyć wszystkie linki na raz
            if st.button("🚀 POBIERZ WSZYSTKO NA RAZ (KLIKNIJ)"):
                js_code = f"""
                <script>
                const links = {links_for_js};
                links.forEach((link, i) => {{
                    setTimeout(() => {{
                        window.open(link, '_blank');
                    }}, i * 1500);
                }});
                </script>
                """
                st.components.v1.html(js_code, height=0)
                st.warning("Upewnij się, że przeglądarka nie blokuje wyskakujących okienek!")

    elif process_btn:
        st.warning("Najpierw wklej linki!")
