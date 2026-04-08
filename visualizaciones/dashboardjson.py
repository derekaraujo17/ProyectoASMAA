import streamlit as st
from visualizaciones.header import render_header
import os
import re 
import unicodedata
import base64

def obtener_pibble_base64(nombreArtista, generoArtista):
    nombreLimpio = ''.join((c for c in unicodedata.normalize('NFD', nombreArtista) if unicodedata.category(c) != 'Mn'))
    nombreLimpio = re.sub(r'[^a-z0-9]', '_', nombreLimpio.lower())
    nombreLimpio = re.sub(r'_+', '_', nombreLimpio).strip('_')
    generoLimpio = ''.join((c for c in unicodedata.normalize('NFD', generoArtista) if unicodedata.category(c) != 'Mn'))
    generoLimpio = re.sub(r'[^a-z0-9]', '_', generoLimpio.lower())
    generoLimpio = re.sub(r'_+', '_', generoLimpio).strip('_')
    
    rutaIdeal = f"frontend/assets/{nombreLimpio}.png"
    rutaGenero = f"frontend/assets/{generoLimpio}.png"

    rutaFinal = rutaIdeal if os.path.exists(rutaIdeal) else rutaGenero
    try:
        with open(rutaFinal, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        return ""


def mostrar_dashboardjson():
    if "mes" in st.query_params:
        pantallaMes = st.query_params["mes"]
        st.session_state["pantallaMes"] = pantallaMes

    render_header()
    rutaCssGlobal = "frontend/estilosGlobales.css"
    try:
        with open(rutaCssGlobal, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True) 
    except FileNotFoundError:
        pass   
    resultados = st.session_state.get("resultados",None)

    if resultados is None:
        st.session_state["pantalla_actual"] = "seleccion"
        st.rerun()
    elif resultados:
        st.session_state["pantalla_actual"] = "dashboardjson"
        cancionesTop1, artistasTop1, resumenFeeling, dfTiempoMensual, top5Canciones, top5Artistas, dfArtistasSemanal, dfCancionesSemanal, tiempoSemanal = resultados

    meses=dfTiempoMensual["añoMesReproduccion"].unique().tolist()

    if not st.session_state.get("pantallaMes"):
        rutaHtmlDashboardjson = "frontend/animacionJson/dashboardjson.html"
        rutaCssDashboardjson = "frontend/animacionJson/dashboardjson.css"
        try:
            with open(rutaHtmlDashboardjson, "r", encoding="utf-8") as f:
                codigoHtml = f.read()
            with open(rutaCssDashboardjson, "r", encoding="utf-8") as f:
                codigoCss = f.read()
            st.markdown(f"<style>{codigoCss}</style>",unsafe_allow_html=True)
        except:
            st.warning(f"Esperando el archivo frontend")
        
        todasLasTarjetas = ""
        for mes in meses:
            urlCancion = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["urlPortada"].iloc[0]
            urlArtista = artistasTop1[artistasTop1["añoMesReproduccion"]==mes]["urlFoto"].iloc[0]
            emojiVibra = resumenFeeling[resumenFeeling["añoMesReproduccion"]==mes]["emoji"].iloc[0]
            porcentaje = dfTiempoMensual[dfTiempoMensual["añoMesReproduccion"]==mes]["porcentajeReloj"].iloc[0]
            minutos = dfTiempoMensual[dfTiempoMensual["añoMesReproduccion"]==mes]["minutosReproducidos"].iloc[0] 
            porcentaje = int(porcentaje*100)
            nombreArtista = artistasTop1[artistasTop1["añoMesReproduccion"]==mes]["artistName"].iloc[0]
            generoArtista = resumenFeeling[resumenFeeling["añoMesReproduccion"]==mes]["vibraDominante"].iloc[0]
            imagenPibbleBase64 = obtener_pibble_base64(nombreArtista,generoArtista)
            tarjetaActual = codigoHtml

            tarjetaActual = tarjetaActual.replace("{{MES_ACTUAL}}",mes)
            tarjetaActual = tarjetaActual.replace("{{URL_CANCION}}",urlCancion)
            tarjetaActual = tarjetaActual.replace("{{URL_ARTISTA}}",urlArtista)
            tarjetaActual = tarjetaActual.replace("{{EMOJI_VIBRA}}",emojiVibra)
            tarjetaActual = tarjetaActual.replace("{{PORCENTAJE}}", str(porcentaje))
            tarjetaActual = tarjetaActual.replace("{{MINUTOS_TOTALES}}",str(minutos))
            tarjetaActual = tarjetaActual.replace("{{IMAGEN_PIBBLE}}",imagenPibbleBase64)
            todasLasTarjetas += tarjetaActual

        gridFinal = f'<div class="contenedor-grid">{todasLasTarjetas}</div>'
        st.markdown(gridFinal, unsafe_allow_html=True)
    else:
        mes = st.session_state["pantallaMes"]
        urlCancion1 = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["urlPortada"].iloc[0]
        nombreCancion1 = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["trackName"].iloc[0]
        nombreArtista1 = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["artistName"].iloc[0]
        if "paso_historia" not in st.session_state:
            st.session_state["paso_historia"] = 1
