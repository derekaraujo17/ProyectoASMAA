import streamlit as st
import time
import random
import base64
import os

@st.cache_data(show_spinner=False)
def ejecutar_motor_json(archivos):
    from logica.motorjson import procesarDatosJson
    return procesarDatosJson(archivos)

def obtener_gif_base64(numero):
    rutasGifs = {
        1: "frontend/animacionCarga/links/intro_KeyboardCat.gif",
        2: "frontend/animacionCarga/links/intro_KeyboardCat.gif",
        3: "frontend/animacionCarga/links/intro_KeyboardCat.gif",
        4: "frontend/animacionCarga/links/intro_KeyboardCat.gif",
        5: "frontend/animacionCarga/links/intro_KeyboardCat.gif"
    }
    ruta = rutasGifs.get(numero, rutasGifs[1])
    try:
        with open(ruta, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/gif;base64, {encoded_string}"
    except FileNotFoundError:
        return ""
def mostrar_pantalla_carga():
    if "analisis_listo" not in st.session_state:
        st.session_state["analisis_listo"] = False
    if "animacion_elegida" not in st.session_state:
        st.session_state["animacion_elegida"] = random.randint(1,5)
    if "ui_renderizada" not in st.session_state:
        st.session_state["ui_renderizada"]=False
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
    contenedorAnimacion = st.empty()
    try: 
        with open(rutaCssCarga, "r", encoding="utf-8") as f:
            codigoCss = f.read()
        with open(rutaHtmlCarga, "r", encoding="utf-8") as f:
            htmlCrudo = f.read()
        with open(rutaJsCarga, "r", encoding="utf-8") as f:
            codigoJs = f.read()
        htmlListo = htmlCrudo.replace("NUMERO", str(numero))
        gif_base64 = obtener_gif_base64(numero)
        htmlListo = htmlCrudo.replace("{{GIF_BASE64}}",gif_base64)
        paqueteCompleto = f"""
        <style>{codigoCss}</style>
        {htmlListo}
        <script>{codigoJs}</script>"""
        contenedorAnimacion.markdown(paqueteCompleto, unsafe_allow_html=True)
        time.sleep(0.2)
    except:
        st.warning("esperando archivos frontend")

    if not st.session_state["ui_renderizada"]:
        st.session_state["ui_renderizada"] = True
        time.sleep(0.5)
        st.rerun()
    if not st.session_state["analisis_listo"]:
        with st.spinner("Pibble está analizando tus datos, esto puede tardar unos segundos..."):
            if st.session_state["motor"] == "motorjson":
                try:
                    resultados = ejecutar_motor_json(st.session_state["jsonValidos"])
                    st.session_state["resultados"] = resultados
                    st.session_state["analisis_listo"] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al analizar los datos: {e}")
            elif st.session_state["motor"] == "motoroauth":
                time.sleep(10)
                st.session_state["analisis_listo"] = True
                st.rerun()
        
    if st.session_state["analisis_listo"]:
        contenedorAnimacion.empty()
        st.success("Pibble terminó el análisis")
        if st.button("Ver resultados"):
            if st.session_state["motor"] == "motorjson":
                st.session_state["pantalla_actual"] = "dashboardjson"
            elif st.session_state["motor"] == "motoroauth":
                st.session_state["pantalla_actual"] = "dashboardoauth"
            
            st.session_state["analisis_listo"] = False
            del st.session_state["animacion_elegida"]
            del st.session_state["ui_renderizada"]
            st.rerun()