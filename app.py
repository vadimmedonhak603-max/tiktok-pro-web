import streamlit as st
import requests
import time

# Konfiguracja - czysta, profesjonalna czerń
st.set_page_config(page_title="TikTok PRO", layout="wide")

st.markdown("""
    <style>
    /* Tło gradientowe z Twojego logo */
    .stApp { 
        background: radial-gradient(circle, #1a1c22 0%, #000000 100%); 
        color: white; 
    }
    header, footer {visibility: hidden;}
    
    /* Pole tekstowe neonowe */
    .stTextArea textarea { 
        background-color: #050505; color: #00d4ff; 
        border: 1px solid #00d4ff; border-radius: 12px;
    }

    /* Karty pobierania - eleganckie i małe */
    .video-row {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #2a2d35;
        padding: 6px 15px;
        border-radius: 8px;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
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

st.title("🛡️ TikTok PRO")

col_in, col_out = st.columns([1, 1])

with col_in:
    st.subheader("📥 Paste Links / Wklej Linki")
    # Automatyczne odświeżanie po wklejeniu (on_change)
    urls_input = st.text_area("URLs:", height=350, placeholder="Paste links here...", key="urls")

with col_out:
    st.subheader("📋 Ready / Gotowe")
    
    if urls_input:
        urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
        
        # Pętla generująca przyciski od razu
        for i, url in enumerate(urls):
            try:
                # Szybkie zapytanie do API
                r = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
                if r.get('code') == 0:
                    link = r['data']['play']
                    
                    # Generowanie małego wiersza z przyciskiem "Blob" (bez otwierania kart)
                    js_code = f"""
                    <script>
                    function startDl_{i}() {{
                        fetch('{link}')
                        .then(r => r.blob())
                        .then(blob => {{
                            const u = window.URL.createObjectURL(blob);
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
                        <span style="color: #00d4ff; font-size: 12px;">#{i+1} Ready / Gotowe</span>
                        <button onclick="startDl_{i}()" class="dl-btn">DOWNLOAD / POBIERZ</button>
                    </div>
                    """
                    st.components.v1.html(js_code, height=45)
                else:
                    st.error(f"Error link #{i+1}")
            except:
                pass
    else:
        st.write("Waiting for links... / Czekam na linki...")

# Przycisk czyszczenia w boku
if st.sidebar.button("Clear All / Wyczyść"):
    st.rerun()
