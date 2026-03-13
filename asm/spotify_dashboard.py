import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import plotly.express as px

# ---------- CONFIGURACIÓN ----------
st.set_page_config(
    page_title="Spotify Wrapped Analyzer",
    page_icon="🎧",
    layout="wide"
)

#titulo de la aplicación y descripción
st.title("🎧 Spotify Wrapped Analyzer")
st.write("Descubre tus artistas más escuchados")

# ---------- BOTÓN ----------
#boton a presionar para conectar con spotify y obtener los datos del usuario
if st.button("Conectar con Spotify"):
#credenciales para conectar con la API de Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="18c9f2493f8e4bc2851dc9b8632c202a",
        client_secret="70e718f19b804805b835a7dce9719842",
        redirect_uri="http://127.0.0.1:8501/",
        scope="user-top-read"
    ))


# limite de artistas a mostrar, en este caso 10
    results = sp.current_user_top_artists(limit=10)

#mostrar los artistas en la interfaz de Streamlit
    st.subheader("🔥 Tus Top Artistas")
#columnas de 5 para mostrar los artistas en una cuadrícula
    cols = st.columns(5)
#iterar sobre los artistas obtenidos y mostrarlos en las columnas correspondientes
    for i, artist in enumerate(results['items']):
        with cols[i % 5]:
            st.image(artist['images'][0]['url'])
            st.markdown(f"**{artist['name']}**")

    st.markdown("---")
    st.subheader("🎧 Tus canciones más escuchadas del mes")




# obtener top canciones del último mes
    top_tracks = sp.current_user_top_tracks(limit=10, time_range="short_term")

    canciones = []
    ranking = []

    for i, track in enumerate(top_tracks['items'], start=1):
        canciones.append(track['name'])
        ranking.append(i)

    df_tracks = pd.DataFrame({
    "Canción": canciones,
    "Ranking": ranking
    })

    df_tracks = df_tracks.sort_values(by="Ranking", ascending=False)

    fig = px.bar(
        df_tracks,
        x="Ranking",
        y="Canción",
        orientation="h",
        color="Ranking",
        color_continuous_scale="Greens"
    )

    fig.update_layout(
        template="plotly_dark",
        title="🎧 Tus canciones más escuchadas del mes",
        xaxis_title="Posición en tu ranking",
        yaxis_title="Canción"
    )

    st.plotly_chart(fig, use_container_width=True)
