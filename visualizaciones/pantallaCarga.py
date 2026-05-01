import streamlit as st
import time
import random
from visualizaciones.header import render_header
from visualizaciones.helpers import leer_externos, obtener_imagen_base64

@st.cache_data(show_spinner=False)
def ejecutar_motor_json(archivos):
    from logica.motorjson import procesarDatosJson
    return procesarDatosJson(archivos)

@st.cache_data(show_spinner=False)
def ejecutar_motor_oauth(token):
    from logica.motoroauth import ticket
    return ticket(token)

def mostrar_pantalla_carga():
    if "analisis_listo" not in st.session_state:
        st.session_state["analisis_listo"] = False
    if "animacion_elegida" not in st.session_state:
        st.session_state["animacion_elegida"] = random.randint(1,7)
    if "ui_renderizada" not in st.session_state:
        st.session_state["ui_renderizada"] = False
    if "tiempo_inicio_carga" not in st.session_state:
        st.session_state["tiempo_inicio_carga"] = None

    numero = st.session_state["animacion_elegida"]    
    try:
        cssGlobal = leer_externos("frontend/estilosGlobales.css")
        st.markdown(f"<style>{cssGlobal}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    if not st.session_state["analisis_listo"]:
        
        contenedorAnimacion = st.empty()
        rutasGifs = {
            1: "frontend/animacionCarga/links/pibble_edn.gif",
            2: "frontend/animacionCarga/links/starkirk.gif",
            3: "frontend/animacionCarga/links/tuff.gif",
            4: "frontend/animacionCarga/links/pibble_edn.gif",
            5: "frontend/animacionCarga/links/starkirk.gif",
            6: "frontend/animacionCarga/links/pibble_edn.gif",
            7: "frontend/animacionCarga/links/tuff.gif"
        }
        rutaGifElegida = rutasGifs.get(numero, rutasGifs[1])
        
        try: 
            codigoCss = leer_externos("frontend/animacionCarga/carga.css")
            htmlCrudo = leer_externos("frontend/animacionCarga/carga.html")
            gif_base64 = obtener_imagen_base64(rutaGifElegida)
            htmlListo = htmlCrudo.replace("NUMERO", str(numero))
            htmlListo = htmlListo.replace("{{GIF_BASE64}}", gif_base64)
            paqueteCompleto = f"<style>{codigoCss}</style>{htmlListo}"
            
            contenedorAnimacion.markdown(paqueteCompleto, unsafe_allow_html=True)
            time.sleep(0.2)
        except:
            st.warning("Esperando archivos frontend")

        if not st.session_state["ui_renderizada"]:
            st.session_state["ui_renderizada"] = True
            st.session_state["tiempo_inicio_carga"] = time.time()
            st.rerun()
            
        with st.spinner():
            if st.session_state["motor"] == "motorjson":
                try:
                    tiempoInicio = time.time()
                    resultados = ejecutar_motor_json(st.session_state["jsonValidos"])
                    st.session_state["resultados"] = resultados
                    tiempoTranscurrido = time.time() - tiempoInicio
                    tiempoMinimo = 10.0
                    
                    if tiempoTranscurrido < tiempoMinimo:
                        tiempoRestante = tiempoMinimo - tiempoTranscurrido
                        time.sleep(tiempoRestante)
                        
                    st.session_state["analisis_listo"] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al analizar los datos: {e}")
                    
            elif st.session_state["motor"] == "motoroauth":
                try:
                    tiempoInicio = time.time()
                    token = st.session_state.get("tokenSpotify")
                    resultados = ejecutar_motor_oauth(token)
                    st.session_state["resultados_oauth"] = resultados
                    tiempoTranscurrido = time.time()-tiempoInicio
                    tiempoMinimo = 10.0
                    if tiempoTranscurrido < tiempoMinimo:
                        tiempoRestante = tiempoMinimo - tiempoTranscurrido
                        time.sleep(tiempoRestante)
                    st.session_state["analisis_listo"] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al conectar con Spotify: {e}")
    else:
        render_header()
        st.success("Pibble terminó el análisis")
        
        if st.button("Ver resultados", use_container_width=True):
            if st.session_state["motor"] == "motorjson":
                st.session_state["pantalla_actual"] = "dashboardjson"
            elif st.session_state["motor"] == "motoroauth":
                st.session_state["pantalla_actual"] = "dashboardoauth"
            
            st.session_state["analisis_listo"] = False
            del st.session_state["animacion_elegida"]
            del st.session_state["ui_renderizada"]
            del st.session_state["tiempo_inicio_carga"]
            st.rerun()