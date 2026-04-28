import streamlit as st

@st.cache_data(show_spinner=False)
def leer_externos(archivo):
    with open (archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    return contenido