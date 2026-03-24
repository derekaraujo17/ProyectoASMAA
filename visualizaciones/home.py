import streamlit as st
import os
from spotipy.oauth2 import SpotifyOAuth #lo que nos dará el inicio de sesión
from dotenv import load_dotenv

load_dotenv()
#ENTREN A SPOTIFY FOR DEVELOPERS Y CAMBIÉN EL PARÁMETRO "Redirect URIs" por : http://127.0.0.1:8501
spotifyOauth=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8501",
    scope="user-top-read user-read-recently-played"
)

def mostrar_pantalla_pibble():
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
    st.write("""#CONVIERTAN EL MOUSE EN UN ESTROPAJO
#HAGAN QUE LA PANZA DE PIBBLE ESTÉ SUCIA
#CUANDO EL USUARIO PASE EL MOUSE/DEDO POR SU PANZA, ESTA SE LIMPIARÁ
#CUANDO ESTÉ LIMPIA, SE DESCUBRIRÁ EL BOTÓN PARA LA AUTENTICACIÓN
#USEN HTML, CSS Y JS SI ES NECESARIO""")
    #botón temporal
    st.link_button("Botón temporarl para iniciar sesión con spotify", urlAutorizacion)
