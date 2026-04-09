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
        cols = st.columns(3) 

        for index, mes in enumerate(meses):
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

            colActual = cols[index%3]
            with colActual:
                st.markdown(tarjetaActual, unsafe_allow_html=True)
                if st.button(f"Ver resumen de{mes}", key=f"btn_{mes}", use_container_width=True):
                    st.session_state["pantallaMes"] = mes
                    st.rerun()
    else:
        mes = st.session_state["pantallaMes"]
        paso = st.session_state.setdefault("paso_historia",1)
        if paso == 1:
            rutaHtmlDiapositiva1="frontend/animacionJson/slideCancion.html"
            with open(rutaHtmlDiapositiva1, "r", encoding="utf-8") as f:
                moldeSlide = f.read()
            urlCancion1 = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["urlPortada"].iloc[0]
            nombreCancion1 = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["trackName"].iloc[0]
            nombreArtista1 = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["artistName"].iloc[0]
            escuchas = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["cantidadEscuchas"].iloc[0]
            slideActual = moldeSlide.replace("{{URL_CANCION}}", urlCancion1)
            slideActual = slideActual.replace("{{NOMBRE_CANCION}}",nombreCancion1)
            slideActual = slideActual.replace("{{NOMBRE_ARTISTA}}",nombreArtista1)
            slideActual = slideActual.replace("{{CANTIDAD_ESCUCHAS}}",str(escuchas))
            st.markdown(slideActual, unsafe_allow_html=True)
            if st.button("Siguiente paso: Tu artista top"):
                st.session_state["paso_historia"] = 2
                st.rerun()
        elif paso == 2:
            rutaHtmlDiapositiva2 = "frontend/animacionJson/slideArtista.html"
            with open(rutaHtmlDiapositiva2, "r", encoding="utf-8") as f:
                moldeSlide = f.read()
            nombreArtista = artistasTop1[artistasTop1["añoMesReproduccion"]==mes]["artistName"].iloc[0]
            urlArtista = artistasTop1[artistasTop1["añoMesReproduccion"]==mes]["urlFoto"].iloc[0]
            generoArtista = resumenFeeling[resumenFeeling["añoMesReproduccion"]==mes]["vibraDominante"].iloc[0]
            imagenPibble = obtener_pibble_base64(nombreArtista, generoArtista)
            minutosArtista = artistasTop1[artistasTop1["añoMesReproduccion"]==mes]["minutosReproducidos"].iloc[0]
            slideActual = moldeSlide.replace("{{IMAGEN_PIBBLE}}", imagenPibble)
            slideActual = slideActual.replace("{{URL_ARTISTA}}",urlArtista)
            slideActual = slideActual.replace("{{NOMBRE_ARTISTA}}", nombreArtista)
            slideActual = slideActual.replace("{{MINUTOS_TOTALES}}", str(minutosArtista))
            st.markdown(slideActual, unsafe_allow_html=True)
            if st.button("Siguiente paso: Tu vibra mensual"):
                st.session_state["paso_historia"] = 3
                st.rerun()
        elif paso == 3:
            rutaHtmlDiapositiva3 = "frontend/animacionJson/slideFeeling.html"
            with open(rutaHtmlDiapositiva3, "r", encoding="utf-8") as f:
                moldeSlide = f.read()
            vibra = resumenFeeling[resumenFeeling["añoMesReproduccion"]==mes]["vibraDominante"].iloc[0]
            emoji = resumenFeeling[resumenFeeling["añoMesReproduccion"]==mes]["emoji"].iloc[0]
            slideActual = moldeSlide.replace("{{EMOJI_VIBRA}}", emoji)
            slideActual = slideActual.replace("{{NOMBRE_VIBRA}}", vibra)
            st.markdown(slideActual, unsafe_allow_html=True)
            if st.button("Siguiente paso: Tu tiempo total de escucha"):
                st.session_state["paso_historia"]=4
                st.rerun()
        elif paso == 4:
            rutaHtmlDiapositiva4 = "frontend/animacionJson/slideTiempo.html"
            with open(rutaHtmlDiapositiva4, "r", encoding="utf-8") as f:
                moldeSlide = f.read()
            minutosTotales = dfTiempoMensual[dfTiempoMensual["añoMesReproduccion"]==mes]["minutosReproducidos"].iloc[0]
            diasTotales = round(minutosTotales/1440,1)
            slideActual = moldeSlide.replace("{{MINUTOS_TOTALES}}",str(minutosTotales))
            slideActual = slideActual.replace("{{DIAS_TOTALES}}",str(diasTotales))
            st.markdown(slideActual, unsafe_allow_html=True)
            if st.button("Resumen completo"):
                st.session_state["paso_historia"] = 5
                st.rerun()
        elif paso == 5:
            rutaHtmlDiapositiva5 = "frontend/animacionJson/slideCompleto.html"
            with open(rutaHtmlDiapositiva5, "r",encoding="utf-8") as f:
                moldeSlide = f.read()
            cancionesDelMes = top5Canciones[top5Canciones["añoMesReproduccion"]==mes]
            htmlListaCanciones = ""
            for index, fila in cancionesDelMes.iterrows():
                urlCancion = fila["urlPortada"]
                nombreCancion = fila["trackName"]
                nombreArtista = fila["artistName"]
                elementoLi = f'<li class="elemento-lista"><img class="slide-completo-lista" src="{urlCancion}"><p class="nombre-cancion">{nombreCancion} de {nombreArtista}</p></li>'
                htmlListaCanciones += elementoLi
            slideActual = moldeSlide.replace("{{MES_ACTUAL}}", mes)
            slideActual = slideActual.replace("{{LISTA_CANCIONES}}", htmlListaCanciones)
            slideActual = slideActual.replace('\n', '')
            st.markdown(slideActual, unsafe_allow_html=True)
            if st.button("Volver al resumen de todos los meses", use_container_width=True):
                del st.session_state["pantallaMes"]
                del st.session_state["paso_historia"]
                st.rerun()
                