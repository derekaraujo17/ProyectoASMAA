import streamlit as st
import os
from spotipy.oauth2 import SpotifyOAuth
import streamlit.components.v1 as components
from dotenv import load_dotenv
from visualizaciones.header import render_header
import base64

#load_dotenv()
spotifyOauth=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8501",
    scope="user-top-read user-read-recently-played"
)

def obtener_imagen_base64(rutaImagen):
    try:
        with open(rutaImagen, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        return ""

def mostrar_pantalla_pibble():
    rutaCssGlobal = "frontend/estilosGlobales.css"
    try: 
        with open(rutaCssGlobal, "r", encoding="utf-8") as f:
            cssGlobal = f.read()
            st.markdown(f"<style>{cssGlobal}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    
    render_header()
    st.title("Spibblepy")
    #después de que spotify apruebe el acceso, devuelve al usuario a la app poniendo un parámetro "?code="
    #cuando eso ocurre, detectamos la palabra, y si la detectamos, sabemos que el usuario ya se autenticó
    if "code" in st.query_params:
        #guardamos el código que spotify regresa en la url  lo guardamos en la variable codigoAutorizacion, un "ticket" que nos dará acceso a los datos
        codigoAutorizacion = st.query_params["code"] #query:params es un diccionario de streamlit que lee la url de la barra superior del navegador
        
        #intercambiamos el código temporal que nos regresa Spotify con Spotipy y nos devuelva la información del token real
        infoToken = spotifyOauth.get_access_token(codigoAutorizacion)

        #guardamos este token en la memoria de la aplicación para poder usarla en siguientes pantallas
        st.session_state["tokenSpotify"] = infoToken["access_token"]

        #limpiamos la url para que el próximo usuario pueda autenticarse sin problema
        st.query_params.clear()
        #actualizamos pantallas
        st.session_state["autenticado"] = True
        st.session_state["pantalla_actual"] = "seleccion"
        st.rerun()
    #la primera vez que entra un usuario
    urlAutorizacion = spotifyOauth.get_authorize_url()
    #botón temporal
    #st.markdown(f'<a href="{urlAutorizacion}" target="_top">Iniciar sesión con Spotify</a>', unsafe_allow_html=True)
    #CONEXIÓN CON EL FRONTEND
    rutaHtml = "frontend/homeJuegoPibble/pibble.html"
    rutaCss = "frontend/homeJuegoPibble/pibble.css"
    rutaJs = "frontend/homeJuegoPibble/pibble.js"
    try:
        with open(rutaHtml, "r", encoding="utf-8") as f:
            codigoHtml = f.read()
        with open(rutaCss, "r", encoding="utf-8") as f:
            codigoCss = f.read()
        with open(rutaJs, "r", encoding="utf-8") as f:
            codigoJs = f.read()
        pibbleSuciob64 = obtener_imagen_base64("frontend/assets/pibble_sucio.png")
        pibbleLimpiob64 = obtener_imagen_base64("frontend/assets/pibble_limpio.png")
        estropajob64 = obtener_imagen_base64("frontend/assets/estropajo.png")
        #variables a reemplazar en html, css, js
        htmlFinal = codigoHtml.replace("urlspotiaqui", urlAutorizacion)
        htmlFinal = htmlFinal.replace("{{PIBBLE_SUCIO}}", pibbleSuciob64)
        htmlFinal = htmlFinal.replace("{{PIBBLE_LIMPIO}}",pibbleLimpiob64)
        codigoCss = codigoCss.replace("{{ESTROPAJO}}", estropajob64)

        paqueteCompleto = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="UTF-8">
        <meta name="color-scheme" content="dark light">
        <style>html, body{{background-color:transparent !important; background:transparent !important; color-scheme:dark; margin:0; padding:0;}}</style>
        <style>{cssGlobal}</style>
        <style>{codigoCss}</style>
        </head>
        <body>
        {htmlFinal}
        <script>{codigoJs}</script>
        </body>
        </html>
        """
        htmlb64 = base64.b64encode(paqueteCompleto.encode('utf-8')).decode('utf-8')
        iframeCode = f'''<iframe
        src="data:text/html;base64,{htmlb64}"
        width="100%"
        height="500px"
        allowtransparency="true"
        style="border:none; background:transparent;"
        sandbox="allow-scripts allow-same-origin allow-top-navigation"
        ></iframe>'''
        st.markdown(iframeCode, unsafe_allow_html=True)    
    except:
        st.warning(f"Esperando el archivo frontend")