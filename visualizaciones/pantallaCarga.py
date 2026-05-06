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
        st.session_state["animacion_elegida"] = random.randint(1, 7)

    if "ui_renderizada" not in st.session_state:
        st.session_state["ui_renderizada"] = False

    numero = st.session_state["animacion_elegida"]

    try:
        cssGlobal = leer_externos("frontend/estilosGlobales.css")
        st.markdown(f"<style>{cssGlobal}</style>", unsafe_allow_html=True)
    except:
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

            htmlListo = htmlCrudo.replace("{{GIF_BASE64}}", gif_base64)

            paqueteCompleto = f"<style>{codigoCss}</style>{htmlListo}"

            contenedorAnimacion.markdown(paqueteCompleto, unsafe_allow_html=True)

            time.sleep(0.2)

        except:
            st.warning("Esperando archivos frontend")
            
        if not st.session_state["ui_renderizada"]:
            st.session_state["ui_renderizada"] = True
            st.rerun()

        with st.spinner():

            if st.session_state["motor"] == "motorjson":
                try:
                    inicio = time.time()

                    resultados = ejecutar_motor_json(st.session_state["jsonValidos"])
                    st.session_state["resultados"] = resultados

                    if time.time() - inicio < 10:
                        time.sleep(10 - (time.time() - inicio))

                    st.session_state["analisis_listo"] = True
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

            elif st.session_state["motor"] == "motoroauth":
                try:
                    inicio = time.time()

                    token = st.session_state.get("tokenSpotify")
                    resultados = ejecutar_motor_oauth(token)
                    st.session_state["resultados_oauth"] = resultados

                    if time.time() - inicio < 10:
                        time.sleep(10 - (time.time() - inicio))

                    st.session_state["analisis_listo"] = True
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

    else:
        render_header()
        st.success("¡Pibble terminó de cocinar!")
        pibbleChef = obtener_imagen_base64("frontend/assets/pibble_chef.png")
        plato = obtener_imagen_base64("frontend/assets/plato.png")
        
        st.markdown(f"""
        <style>
        div[data-testid="stAlert"] {{
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .contenedor-chef {{
            display:flex;
            justify-content:center;
            margin-top:20px;
        }}
            
        .escena {{
            position:relative;
            width:350px;
        }}

        .chef {{
            width:100%;
            transform: scale(1.3) translateY(10px);
            
        }}

        .plato {{
            position:absolute;
            bottom:0;
            left:50%;
            transform:translateX(-50%);
            width:80%;
        }}

        .boton-overlay {{
            position:absolute;
            bottom:35px;
            left:50%;
            transform:translateX(-50%);
            width:60%;
        }}

        .boton-overlay button {{
            width:100%;
            padding:10px;
            border: none;
            border-radius:20px;
            background:linear-gradient(45deg,#8a2be2,#a855f7);
            color:white;
            font-family:'Press Start 2P';
            cursor:pointer;
        }}
        </style>
        
        <div class="contenedor-chef">
            <div class="escena">
                <img src="{pibbleChef}" class="chef">
                <img src="{plato}" class="plato">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1], vertical_alignment="center")
        st.markdown("""
        <style>
        div[data-testid="stButton"] {
            margin-top: -100px;
            margin-left: 232px;
            display: flex;
            justify-content: center;
        }
        
        div[data-testid="stButton"] button {
            width: 220px !important;
            background: linear-gradient(135deg, #1DB954, #1ed760) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-family: 'Press Start 2P', cursive !important;
            padding: 10px;
            box-shadow:
                0 0 15px rgba(29, 185, 84, 0.6),
                0 0 30px rgba(29, 185, 84, 0.4),
                0 8px 20px rgba(0,0,0,0.6);
            font-size: 10px !important;
            transition: all 0.3s ease !important;
            animation: glowPulse 2s infinite alternate;
        }
        div[data-testid="stButton"] button:hover {
            transform: scale(1.08);
            filter: brightness(1.2);
            box-shadow: 
                0 0 25px rgba(29, 185, 84, 0.9),
                0 0 50px rgba(29, 185, 84, 0.6),
                0 10px 25px rgba(0,0,0,0.7);
        }
        
        @keyframes glowPulse {
            from { 
                box-shadow: 
                    0 0 10px rgba(29,185,84,0.4),
                    0 5px 15px rgba(0,0,0,0.5);
            }
            to { 
                box-shadow: 
                    0 0 35px rgba(29,185,84,0.9),
                    0 10px 25px rgba(0,0,0,0.7);
            }
        }
        
        </style>
        """, unsafe_allow_html=True)
        with col2:
            if st.button("SERVIR RESULTADOS"):

                if st.session_state["motor"] == "motorjson":
                    st.session_state["pantalla_actual"] = "dashboardjson"
                    
                elif st.session_state["motor"] == "motoroauth":
                    st.session_state["pantalla_actual"] = "dashboardoauth"
                
                st.session_state["analisis_listo"] = False
                st.session_state["animacion_elegida"]
                st.session_state["ui_renderizada"]

                st.rerun()