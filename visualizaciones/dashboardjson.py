import streamlit as st
from visualizaciones.header import render_header

def mostrar_dashboardjson():
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
        tarjetaActual = codigoHtml

        tarjetaActual = tarjetaActual.replace("{{MES_ACTUAL}}",mes)
        tarjetaActual = tarjetaActual.replace("{{URL_CANCION}}",urlCancion)
        tarjetaActual = tarjetaActual.replace("{{URL_ARTISTA}}",urlArtista)
        tarjetaActual = tarjetaActual.replace("{{EMOJI_VIBRA}}",emojiVibra)
        tarjetaActual = tarjetaActual.replace("{{PORCENTAJE}}", str(porcentaje))
        tarjetaActual = tarjetaActual.replace("{{MINUTOS_TOTALES}}",str(minutos))

        todasLasTarjetas += tarjetaActual

    gridFinal = f'<div class="contenedor-grid">{todasLasTarjetas}</div>'
    st.markdown(gridFinal, unsafe_allow_html=True)
        
        