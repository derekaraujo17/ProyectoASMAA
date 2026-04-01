import streamlit as st
import time

def mostrar_pantalla_carga():
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
        with open(rutaCssCarga, "r",encoding="utf-8") as f:
            codigoCss = f.read()
        with open(rutaHtmlCarga, "r", encoding="utf-8") as f:
            codigoHtml = f.read()
        with open(rutaJsCarga, "r", encoding="utf-8") as f:
            codigoJs = f.read()
        paqueteCompleto = f"""
        <style>{codigoCss}</style>
        {codigoHtml}
        <script>{codigoJs}</script>
        """
        st.markdown(paqueteCompleto,unsafe_allow_html=True)
    except:
        st.warning(f"Esperando el archivo frontend")
    if st.session_state["motor"] == "motorjson":
        time.sleep(10)
        st.session_state["pantalla_actual"] = "dashboardjson"
        st.write("dashboard json")
        st.rerun()
    elif st.session_state["motor"] == "motoroauth":
        time.sleep(10)
        st.session_state["pantalla_actual"] = "dashboardoauth"
        st.write("dashboard oauth")
        st.rerun()
