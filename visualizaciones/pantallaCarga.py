import streamlit as st
import time
import random

def mostrar_pantalla_carga():
    if "analisis_listo" not in st.session_state:
        st.session_state["analisis_listo"] = False
    if "animacion_elegida" not in st.session_state:
        st.session_state["animacion_elegida"] = random.randint(1,5)
    
    numero = st.session_state["animacion_elegida"]
    rutaCssCarga = "frontend/animacionCarga/carga.css"
    rutaHtmlCarga = "frontend/animacionCarga/carga.html"
    rutaJsCarga = "frontend/animacionCarga/carga.js"
    rutaCssGlobal = "frontend/estilosGlobales.css"
    try:
        with open(rutaCssGlobal, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    try: 
        with open(rutaCssCarga, "r", encoding="utf-8") as f:
            codigoCss = f.read()
        with open(rutaHtmlCarga, "r", encoding="utf-8") as f:
            htmlCrudo = f.read()
        with open(rutaJsCarga, "r", encoding="utf-8") as f:
            codigoJs = f.read()
        
        htmlListo = htmlCrudo.replace("NUMERO", str(numero))

        paqueteCompleto = f"""
        <style>{codigoCss}</style>
        {htmlListo}
        <script>{codigoJs}</script>"""
        st.markdown(paqueteCompleto, unsafe_allow_html=True)
    except:
        st.warning("esperando archivos frontend")

    if not st.session_state["analisis_listo"]:
        if st.session_state["motor"] == "motorjson":
            time.sleep(10)
            st.session_state["analisis_listo"] = True
            st.rerun()
        elif st.session_state["motor"] == "motoroauth":
            time.sleep(10)
            st.session_state["analisis_listo"] = True
            st.rerun()
    
    if st.session_state["analisis_listo"]:
        st.success("Pibble terminó el análisis")
        if st.button("Ver resultados"):
            if st.session_state["motor"] == "motorjson":
                st.session_state["pantalla_actual"] = "dashboardjson"
            elif st.session_state["motor"] == "motoroauth":
                st.session_state["pantalla_actual"] = "dashboardoauth"
            
            st.session_state["analisis_listo"] = False
            del st.session_state["animacion_elegida"]
            st.rerun()