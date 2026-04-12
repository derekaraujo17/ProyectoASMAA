import streamlit as st
from visualizaciones.header import render_header
import base64

def obtener_imagen_base64(rutaImagen):
     try:
        with open(rutaImagen, "rb") as imageFile:
           encoded_string = base64.b64encode(imageFile.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
     except FileNotFoundError:
        return ""

def cargarArchivos(archivosSubidos):
            archivosValidos=[]
            if len(archivosSubidos)>= 1:
                archivosValidos = [archivo for archivo in archivosSubidos if "StreamingHistory_music" in archivo.name]
            return archivosValidos
        
def mostrar_pantalla_botones():
    render_header()
    st.title("Elegir la opción de los datos")
    pibbleFondob64 = obtener_imagen_base64("frontend/assets/pibble_brazos.png")

    rutaCssGlobal="frontend/estilosGlobales.css"
    rutaCssSeleccion="frontend/seleccion.css"
    cssInyectado = f"""<style>:root {{--fondo-pibble: url('pibbleFondob64')}}"""
    try:
        with open(rutaCssGlobal,"r",encoding="utf-8") as f:
            cssInyectado += f.read() + "\n"
    except FileNotFoundError:
        pass
    try:
        with open(rutaCssSeleccion, "r", encoding="utf-8") as f:
            cssInyectado += f.read() + "\n"
    except FileNotFoundError:
        st.warning("Esperando el archivo frontend")
    cssInyectado += "</style>"
    st.markdown(cssInyectado, unsafe_allow_html=True)

    col1, colCentro, col2 = st.columns([1, 1.5, 1])

    with col1:
        #botón json
        st.markdown("<h3 class='titulo-columna'>Analizar historial json</h3>",unsafe_allow_html=True)
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
    with colCentro:
        st.empty()
    with col2:
        #botón oauth
        st.markdown("<h3 class='titulo-columna'>Conectar con spotify</h3>",unsafe_allow_html=True)
        if st.button("Datos actuales", disabled=len(jsonValidos)>0):
            st.session_state["motor"] = "motoroauth"
            st.session_state["pantalla_actual"] = "pantallaCarga"
            st.rerun()