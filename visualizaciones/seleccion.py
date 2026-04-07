import streamlit as st
from visualizaciones.header import render_header

def cargarArchivos(archivosSubidos):
            archivosValidos=[]
            if len(archivosSubidos)>= 1:
                archivosValidos = [archivo for archivo in archivosSubidos if "StreamingHistory_music" in archivo.name]
            return archivosValidos
        
def mostrar_pantalla_botones():
    #conexión con css
    rutaCssGlobal="frontend/estilosGlobales.css"
    try:
        with open(rutaCssGlobal,"r",encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    rutaCssSeleccion="frontend/seleccion.css"
    try:
        with open(rutaCssSeleccion, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Esperando el archivo frontend")
    st.title("Elegir la opción de los datos")
    render_header()
    col1, col2 = st.columns(2)

    with col1:
        #botón json
        st.markdown("<h3 class='titulo-columna'>Analizar historial json</h3>",unsafe_allow_html=True)
        st.markdown("<img src='fotobotonjson' class='foto-seleccion-json'>",unsafe_allow_html=True)
        archivosSubidos = st.file_uploader("Sube tus archivos JSON", accept_multiple_files=True, type=["json"])
        jsonValidos = cargarArchivos(archivosSubidos)
        if len(jsonValidos)>=1:
            if st.button("Analizar mis archivos"):
                st.session_state["jsonValidos"] = jsonValidos
                st.session_state["motor"] = "motorjson"
                st.session_state["pantalla_actual"] = "pantallaCarga"
                st.rerun()
        elif (len(archivosSubidos)>0):
             st.error("Por favor, sube los archivos de 'StreamingHistory_music' que descargaste de spotify")
    with col2:
        #botón oauth
        st.markdown("<h3 class='titulo-columna'>Conectar con spotify</h3>",unsafe_allow_html=True)
        st.markdown("<img src='fotobotonoauth' class='foto-seleccion-oauth'>",unsafe_allow_html=True)
        if st.button("Datos actuales", disabled=len(jsonValidos)>0):
            st.session_state["motor"] = "motoroauth"
            st.session_state["pantalla_actual"] = "pantallaCarga"
            st.rerun()