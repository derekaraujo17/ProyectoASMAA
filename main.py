from dotenv import load_dotenv
import os

load_dotenv()
import streamlit as st
from visualizaciones import home, seleccion, dashboardjson, dashboardoauth, pantallaCarga

#ESTUDIEN EL CONCEPTO BÁSICO DEL BACKEND WEB EN STREAMLIT: LA MEMORIA SE SESIÓN (st.session_state)

# inicialización de la memoria (st.session_state)
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if "pantalla_actual" not in st.session_state:
    st.session_state["pantalla_actual"] = "home"

#navegación
#se chequea la libreta y se muestra la pantalla correspondiente
if st.session_state["pantalla_actual"] == "home":
    home.mostrar_pantalla_pibble()

elif st.session_state["pantalla_actual"] == "seleccion":
    seleccion.mostrar_pantalla_botones()

elif st.session_state["pantalla_actual"] == "pantallaCarga":
    pantallaCarga.mostrar_pantalla_carga()

elif st.session_state["pantalla_actual"] == "dashboardjson":
    st.title("dashboard de json")
#cuando creemos el dashboard de oauth
elif st.session_state["pantalla_actual"] == "dashboardoauth":
    st.title("dashboard de oauth")