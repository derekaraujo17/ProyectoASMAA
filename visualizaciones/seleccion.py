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
    
    # Asegúrate de que la ruta sea correcta
    pibbleFondob64 = obtener_imagen_base64("frontend/assets/pibble_brazos.png")
    rutaCssGlobal = "frontend/estilosGlobales.css"
    rutaCssSeleccion = "frontend/seleccion.css"

    estilos_finales = f"""
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        * {{
            font-family: 'Press Start 2P', cursive !important;
        }}
        .pibble-master-container {{
            background-image: url('{pibbleFondob64}');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center top;
            width: 100%;
            height: 90vh;
            margin: 0 auto;
            position: relative;
        }}
        .pibble-master-container [data-testid="stHorizontalBlock"] {{
            position: absolute;
            top: 15%; 
            width: 100%;
            height: 75%;
        }}
        .espaciador-manos {{
            margin-top: auto;
            padding-bottom: 90px; /* Incrementado para asegurar que baje a la palma */
            display: flex;
            justify-content: center;
        }}
        div.pildora-roja [data-testid="stButton"] > button {{
            background: radial-gradient(circle, #ff1111 0%, #770000 100%) !important;
            background-image: radial-gradient(circle, #ff1111 0%, #770000 100%) !important;
            border: 2px solid #ffffff !important;
            border-radius: 50px !important;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.6) !important;
            color: white !important;
        }}
        div.pildora-azul [data-testid="stButton"] > button {{
            background: radial-gradient(circle, #0066ff 0%, #000066 100%) !important;
            background-image: radial-gradient(circle, #0066ff 0%, #000066 100%) !important;
            border: 2px solid #ffffff !important;
            border-radius: 50px !important;
            box-shadow: 0 0 20px rgba(0, 100, 255, 0.6) !important;
            color: white !important;
            margin-left: 40px !important; 
        }}
        div.pildora-roja [data-testid="stButton"] > button:hover {{
            background: #ff0000 !important;
            box-shadow: 0 0 35px rgba(255, 0, 0, 0.9) !important;
            transform: scale(1.05) !important;
        }}
        div.pildora-azul [data-testid="stButton"] > button:hover {{
            background: #0044ff !important;
            box-shadow: 0 0 35px rgba(0, 100, 255, 0.9) !important;
            transform: scale(1.05) !important;
        }}
        
        div.pildora-roja button p, div.pildora-azul button p {{
            color: white !important;
        }}
        .pildora-azul {{
            display: flex;
            justify-content: flex-start;
            width: 100%;
        }}
    """
    
    try:
        with open(rutaCssGlobal, "r", encoding="utf-8") as f: estilos_finales += f.read() + "\n"
    except FileNotFoundError: pass
    try:
        with open(rutaCssSeleccion, "r", encoding="utf-8") as f: estilos_finales += f.read() + "\n"
    except FileNotFoundError: pass

    st.markdown(f"<style>{estilos_finales}</style>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:white; font-size:18px; margin-top:10px;'>¿QUÉ REALIDAD ELIGES?</h1>", unsafe_allow_html=True)

    st.markdown('<div class="pibble-master-container">', unsafe_allow_html=True)
    col_izq, col_centro, col_der = st.columns([1.2, 0.6, 1.2])

    with col_izq:
        st.markdown('<div class="contenedor-pastilla">', unsafe_allow_html=True)
        st.markdown('<div class="lore-matrix" style="color: #ff4b4b;">TOMAS LA PASTILLA ROJA... Y TE ENSEÑARÉ QUÉ TAN PROFUNDO LLEGA EL AGUJERO DE TUS DATOS. LA VERDAD ABSOLUTA SOBRE TU MÚSICA.</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="espaciador-manos">', unsafe_allow_html=True)
        archivosSubidos = st.file_uploader("Subir", accept_multiple_files=True, type=["json"], key="up_j", label_visibility="collapsed")
        jsonValidos = cargarArchivos(archivosSubidos)
        
        if len(jsonValidos) >= 1:
            st.markdown('<div class="pildora-roja">', unsafe_allow_html=True)
            if st.button("ANALIZAR DATOS", key="btn_json"):
                st.session_state.update({"jsonValidos": jsonValidos, "motor": "motorjson", "pantalla_actual": "pantallaCarga"})
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_centro:
        st.empty() 

    with col_der:
        st.markdown('<div class="contenedor-pastilla">', unsafe_allow_html=True)
        st.markdown('<div class="lore-matrix" style="color: #4bb4ff;">TOMAS LA PASTILLA AZUL... DESPIERTAS Y CREES LO QUE QUIERAS CREER. TE QUEDARÁS EN LA SUPERFICIE DEL PRESENTE.</div>', unsafe_allow_html=True)
        
        # Aquí envolvemos el botón en el espaciador para que baje a la mano
        st.markdown('<div class="espaciador-manos">', unsafe_allow_html=True)
        st.markdown('<div class="pildora-azul">', unsafe_allow_html=True)
        if st.button("DATOS ACTUALES", key="btn_oauth", disabled=len(jsonValidos) > 0):
            st.session_state.update({"motor": "motoroauth", "pantalla_actual": "pantallaCarga"})
            st.rerun()
        st.markdown('</div></div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)