if st.button("🚀 URUCHOM AUTOMATYCZNE POBIERANIE WSZYSTKIEGO"):
            # Nowy, lepszy skrypt, który wymusza pobieranie bez otwierania kart
            js_code = f"""
            <script>
            const links = {st.session_state.links};
            links.forEach((link, i) => {{
                setTimeout(() => {{
                    fetch(link)
                        .then(resp => resp.blob())
                        .then(blob => {{
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.style.display = 'none';
                            a.href = url;
                            a.download = `tiktok_pro_${{i+1}}.mp4`;
                            document.body.appendChild(a);
                            a.click();
                            window.URL.revokeObjectURL(url);
                        }})
                        .catch(() => window.open(link, '_blank')); // Rezerwowy sposób
                }}, i * 2000);
            }});
            </script>
            """
            st.components.v1.html(js_code, height=0)
            st.info("Pobieranie w toku... Sprawdź dolny pasek przeglądarki.")
