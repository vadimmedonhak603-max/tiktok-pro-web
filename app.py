try:
                    # Nowy silnik celowany prosto w TikToka
                    api_url = f"https://www.tikwm.com/api/?url={url}"
                    res = requests.get(api_url).json()
                    
                    if res.get('code') == 0: # 0 oznacza sukces w tym API
                        data = res.get('data')
                        video_url = data.get('play') # Video bez watermarku
                        title = data.get('title', f'Film {index+1}')
                        
                        st.markdown(f"<div class='video-card'>", unsafe_allow_html=True)
                        st.success(f"✅ {title}")
                        st.video(video_url)
                        st.markdown(f"[📥 POBIERZ TEN FILM BEZ LOGO]({video_url})")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Film {index+1}: Serwer zajęty lub link wygasł.")
                    
                    time.sleep(2) # Bezpieczna przerwa
