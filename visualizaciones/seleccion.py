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
    archivosValidos = []
    if len(archivosSubidos) >= 1:
        archivosValidos = [archivo for archivo in archivosSubidos if "StreamingHistory_music" in archivo.name]
    return archivosValidos

def mostrar_pantalla_botones():
    render_header()
    
    pibbleFondob64 = obtener_imagen_base64("frontend/assets/pibble_brazos.png")
    css_variable_fondo = f"""
    <style>
    :root {{
        --fondo-pibble: url('{pibbleFondob64}');
    }}
    </style>
    """
    st.markdown(css_variable_fondo, unsafe_allow_html=True)

    try:
        with open("frontend/estilosGlobales.css", "r", encoding="utf-8") as f: 
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        with open("frontend/seleccion.css", "r", encoding="utf-8") as f: 
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError: 
        pass

    st.markdown("<h1 class='titulo-seleccion'>¿QUÉ REALIDAD ELIGES?</h1>", unsafe_allow_html=True)

    col_izq, col_centro, col_der = st.columns([1.2, 0.6, 1.2])

    with col_izq:
        st.markdown('<div class="lore-matrix texto-rojo">TOMAS LA PASTILLA ROJA... Y TE ENSEÑARÉ QUÉ TAN PROFUNDO LLEGA EL AGUJERO DE TUS DATOS. LA VERDAD ABSOLUTA SOBRE TU MÚSICA.</div>', unsafe_allow_html=True)
        
        archivosSubidos = st.file_uploader("Sube tus JSON", accept_multiple_files=True, type=["json"], key="up_j", label_visibility="collapsed")
        jsonValidos = cargarArchivos(archivosSubidos)
        
        if len(jsonValidos) >= 1:
            if st.button("ANALIZAR DATOS", key="btn_json", use_container_width=True):
                st.session_state.update({"jsonValidos": jsonValidos, "motor": "motorjson", "pantalla_actual": "pantallaCarga"})
                st.rerun()

    with col_centro:
        st.empty() 

    with col_der:
        st.markdown('<div class="lore-matrix texto-azul">TOMAS LA PASTILLA AZUL... DESPIERTAS Y CREES LO QUE QUIERAS CREER. TE QUEDARÁS EN LA SUPERFICIE DEL PRESENTE.</div>', unsafe_allow_html=True)
        
        if st.button("DATOS ACTUALES", key="btn_oauth", disabled=len(jsonValidos) > 0, use_container_width=True):
            st.session_state.update({"motor": "motoroauth", "pantalla_actual": "pantallaCarga"})
            st.rerun()