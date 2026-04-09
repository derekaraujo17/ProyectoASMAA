import streamlit as st
import time
import random

@st.cache_data(show_spinner=False)
def ejecutar_motor_json(archivos):
    from logica.motorjson import procesarDatosJson
    return procesarDatosJson(archivos)

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
    contenedorAnimacion = st.empty()
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
        contenedorAnimacion.markdown(paqueteCompleto, unsafe_allow_html=True)
        time.sleep(0.2)
    except:
        st.warning("esperando archivos frontend")

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
            st.rerun()