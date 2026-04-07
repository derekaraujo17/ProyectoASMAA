import streamlit as st

resultados = st.session_state.get("resultados",None)

if resultados is None:
    st.session_state["pantalla_actual"] = "seleccion"
    st.rerun()
elif resultados:
    st.session_state["pantalla_actual"] = "dashboardjson"
    cancionesTop1, artistasTop1, resumenFeeling, dfTiempoMensual, top5Canciones, top5Artistas, dfArtistasSemanal, dfCancionesSemanal, tiempoSemanal = resultados

meses=dfTiempoMensual["añoMesReproduccion"].unique().tolist()

for mes in meses:
    urlCancion = cancionesTop1[cancionesTop1["añoMesReproduccion"]==mes]["urlPortada"].iloc[0]
    urlArtista = artistasTop1[artistasTop1["añoMesReproduccion"]==mes]["urlFoto"].iloc[0]
    emojiVibra = resumenFeeling[resumenFeeling["añoMesReproduccion"]==mes]["emoji"].iloc[0]
    minutosTotales = dfTiempoMensual[dfTiempoMensual["añoMesReproduccion"]==mes]["porcentajeReloj"].iloc[0] 