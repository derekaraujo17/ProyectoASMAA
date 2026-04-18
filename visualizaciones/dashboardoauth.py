import streamlit as st
import base64
from datetime import datetime
from visualizaciones.header import render_header

def mostrar_dashboardoauth():
    render_header()
    datosTicket = st.session_state.get("resultados_oauth")

    if not datosTicket:
        st.error("No hay datos de spotify. Volviendo a la pantalla anterior...")
        st.session_state["pantalla_actual"] = "seleccion"
        st.rerun()
    rutaCssGlobal = "frontend/estilosGlobales.css"
    rutaHtmlTicket = "frontend/animacionOauth/ticket.html"
    rutaCssTicket = "frontend/animacionOauth/ticket.css"
    try:
        with open(rutaCssGlobal, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    try:
        with open(rutaHtmlTicket, "r", encoding="utf-8") as f:
            moldeHtml = f.read()
        with open(rutaCssTicket, "r", encoding="utf-8") as f:
            codigoCss = f.read()
    except FileNotFoundError:
        st.warning("Esperando archivos frontend")
        return
    htmlListaCanciones = ""
    for index, cancion in enumerate(datosTicket):
        renglon=f"""
        <div class="ticket-fila">
        <span class="ticket-num">{(index+1):02d}</span>
        <div class="ticket-info">
        <span class="ticket-cancion">{cancion["nombre"]}</span>
        <span class="ticket-artista">{cancion["artista"]}</span>
        </div>
        <span class="ticket-duracion"{cancion["duracion"]}></span>
        </div>
        """
        htmlListaCanciones += renglon
    fechaHoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    htmlFinal = moldeHtml.replace("{{FECHA_HOY}}",fechaHoy)
    htmlFinal = htmlFinal.replace("{{CANTIDAD_ITEMS}}", str(len(datosTicket)))
    htmlFinal = htmlFinal.replace("{{LISTA_CANCIONES}}", htmlListaCanciones)
    st.markdown(f"<style>{codigoCss}</style>",unsafe_allow_html=True)
    st.markdown(htmlFinal, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin:40px 0;'>",unsafe_allow_html=True)
    if st.button("Volver a elegir análisis",use_container_width=True):
        st.session_state["pantalla_actual"] = "seleccion"
        del st.session_state["resultados_oauth"]
        st.rerun()
