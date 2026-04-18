import spotipy
import pandas as pd
from datetime import datetime

def ticket(token):
    try:
        sp = spotipy.Spotify(auth=token)
        historialCrudo = sp.current_user_recently_played(limit=15)
        cancionesTicket = []
        for item in historialCrudo["items"]:
            track = item["track"]
            duracionMs = track["duration_ms"]
            minutos = duracionMs//60000
            segundos = (duracionMs % 60000) // 1000
            duracion = f"{minutos}:{segundos:02d}"
            playedAt = item["played_at"]
            fechaObj = datetime.strptime(playedAt, "%Y-%m-%dT%H:%M:%S.%fZ")
            fechaFormat = fechaObj.strftime("%d/%m/%Y - %I:%M %p")
            cancionesTicket.append({
                "nombre":track["name"],
                "artista":track["artists"][0]["name"],
                "duracion":duracion,
                "fecha":fechaFormat
            })
        return cancionesTicket
    except Exception as e:
        print(f"Error en motor Oauth: {e}")
        return None