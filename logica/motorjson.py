import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pylast
from collections import Counter
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tabulate import tabulate
import os
from dotenv import load_dotenv

load_dotenv()

pd.set_option('display.width', 1000)     
pd.set_option('display.max_colwidth', 35)

#credenciales de spotify
clientId = os.getenv("SPOTIFY_CLIENT_ID")
clientSecret = os.getenv("SPOTIFY_CLIENT_SECRET")
credenciales = SpotifyClientCredentials(client_id=clientId,client_secret=clientSecret)
sp = spotipy.Spotify(auth_manager=credenciales)

#credenciales de last.fm
apiKey = os.getenv("LASTFM_API_KEY")
apiSecret = os.getenv("LASTFM_API_SECRET")
network = pylast.LastFMNetwork(api_key=apiKey, api_secret=apiSecret)

#MÓDULO 1: "Historial completo". Utiliza datos json

def cargArchivos(ruta_carpeta):
    #convertimor la ruta de acceso en un objeto Path
    carpeta = Path(ruta_carpeta)
    #buscamos los archivos necesarios
    archivosJson = list(carpeta.glob("*StreamingHistory_music*.json"))
    #devolvemos los archivos necesarios
    return archivosJson

root = tk.Tk()
root.withdraw()
rutaElegida = filedialog.askdirectory(title="Selecciona la carpeta de los datos de spotify")
archivosEncontrados = cargArchivos(rutaElegida)

listadf = []
for archivo in archivosEncontrados:
    dfTemporal = pd.read_json(archivo)
    listadf.append(dfTemporal)
dfSpotify = pd.concat(listadf, ignore_index=True)

#limpieza de canciones que no sirven
umbralMs = 30000 #umbral de tiempo mínimo de reproducción
filasAntes = len(dfSpotify)
dfLimpio = dfSpotify[dfSpotify["msPlayed"]>=umbralMs]
filasDespues = len(dfLimpio)
print(f"Líneas originales: {filasAntes}")
print(f"Líneas después de limpieza: {filasDespues}")
print(f"Canciones eliminadas: {filasAntes - filasDespues}")

#se hace una copia del df para no modificar el original
dfLimpio = dfLimpio.copy()
#creación de columnas dentro de este df copia para obtener mes, día y hora de reproducción, usando la columna "endTime" como referencia
dfLimpio["endTime"] = pd.to_datetime(dfLimpio["endTime"])
dfLimpio["mesReproduccion"] = dfLimpio["endTime"].dt.month
dfLimpio["horaReproduccion"] = dfLimpio["endTime"].dt.hour
dfLimpio["diaSemana"] = dfLimpio["endTime"].dt.day_name()
dfLimpio["semanaReproduccion"] = dfLimpio["endTime"].dt.isocalendar().week
dfLimpio["msPlayed"] = dfLimpio["msPlayed"]/60000
dfLimpio = dfLimpio.rename(columns={"msPlayed":"minutosReproducidos"})
dfLimpio["minutosReproducidos"]=dfLimpio["minutosReproducidos"].round(0).astype(int)

#TIEMPO DE ESCUCHA MENSUAL
#agrupación por mes de reproducción y suma del tiempo de reproducción, obteniendo así el total de escucha por mes
dfTiempoMensual = dfLimpio.groupby("mesReproduccion")["minutosReproducidos"].sum().reset_index() #esto regresa una serie donde el índice será el mes, y el valor es la suma de los ms

#ARTISTAS MÁS ESCUCHADOS
#agrupación por artistas más escuchados
dfArtistasMensual = dfLimpio.groupby(["mesReproduccion","artistName"])["minutosReproducidos"].sum().reset_index()
dfArtistasMensual =dfArtistasMensual.sort_values(by=["mesReproduccion","minutosReproducidos"],ascending=[True,False])
top5Artistas =dfArtistasMensual.groupby("mesReproduccion").head()

#CANCIONES MÁS ESCUCHADAS
dfCancionesMensual = dfLimpio.groupby(["mesReproduccion","trackName","artistName"]).agg(
    totalMinutos = ("minutosReproducidos","sum"),
    cantidadEscuchas = ("trackName","count")
).reset_index()
dfCancionesMensual=dfCancionesMensual.sort_values(by=["mesReproduccion","totalMinutos"],ascending=[True,False])
top5Canciones=dfCancionesMensual.groupby("mesReproduccion").head()

#RESUMEN SEMANAL
dfCancionesSemanal = dfLimpio.groupby(["semanaReproduccion","trackName","artistName"]).agg(
    totalMinutos = ("minutosReproducidos","sum"),
    cantidadEscuchas = ("trackName","count")
).reset_index()
dfCancionesSemanal = dfCancionesSemanal.sort_values(by=["semanaReproduccion","totalMinutos"],ascending=[True,False])
resumenSemanal = dfCancionesSemanal.groupby("semanaReproduccion").head()

#FEELING MENSUAL
memoriaGeneros={}
top20CancionesMensual = dfCancionesMensual.groupby("mesReproduccion").head(20).copy()
top20CancionesMensual["generos"] = ""
for indice, fila in top20CancionesMensual.iterrows():
    artista=fila["artistName"]
    #memoria para evitar bloqueos
    if artista in memoriaGeneros:
        top20CancionesMensual.at[indice,"generos"] = memoriaGeneros[artista]
        continue
    try:
        artista_lastfm = network.get_artist(artista)
        top_tags = artista_lastfm.get_top_tags(limit=5)
        listaGeneros = [tag.item.get_name().lower() for tag in top_tags]
        textoGeneros = ", ".join(listaGeneros) if listaGeneros else "sin clasificar"
        top20CancionesMensual.at[indice,"generos"] = textoGeneros
        memoriaGeneros[artista] = textoGeneros
    except Exception as e:
        top20CancionesMensual.at[indice,"generos"] = "no encontrado"
        memoriaGeneros[artista] = "no encontrado"
feelingMensual = top20CancionesMensual.groupby("mesReproduccion")[["generos"]].agg(list).reset_index()

#agrupación de los géneros
#diccionario que tomará los géneros necesarios para cada tipo de etiqueta
diccionarioVibras = {
    # --- CULTURA HIP-HOP Y CALLE ---
    "🎤 Rap & Hip-Hop": ["rap", "hip-hop", "hip hop", "boom bap", "underground hip-hop", "conscious hip hop", "east coast", "west coast"],
    "🔥 Trap & Drill": ["trap", "drill", "emo rap", "cloud rap", "southern hip hop", "atlanta"],
    
    # --- URBANO Y REGIONAL LATINO ---
    "🥵 Urbano Latino": ["reggaeton", "dembow", "latin trap", "urbano latino", "perreo"],
    "🌮 Regional & Corridos": ["corridos tumbados", "corridos", "nortenas", "regional mexicano", "banda", "mariachi", "ranchera", "mexico"],
    "🌴 Tropical & Fiestero": ["salsa", "cumbia", "bachata", "merengue", "tropical", "cumbia sonidera"],
    
    # --- POP Y TENDENCIAS ---
    "🪩 Pop Mainstream": ["pop", "dance pop", "electropop", "top 40", "teen pop", "commercial"],
    "🌸 K-Pop & Asiático": ["k-pop", "j-pop", "korean", "japanese", "anime", "idol"],
    
    # --- NOSTALGIA Y ROMANCE ---
    "🍷 Romántico & Cortavenas": ["bolero", "baladas", "romantico", "latin pop", "amor", "jose jose", "spanish"],
    "📻 Nostalgia Retro": ["70s", "80s", "90s", "00s", "disco", "oldies", "retro", "classic"],
    
    # --- ENERGÍA Y CLUB ---
    "⚡ Electrónica & Club": ["electronic", "house", "techno", "edm", "dance", "trance", "dubstep", "drum and bass", "electro"],
    
    # --- GUITARRAS Y BATERÍAS ---
    "🎸 Rock Clásico & Hard": ["rock", "classic rock", "hard rock", "blues rock", "arena rock"],
    "🖤 Metal & Oscuridad": ["metal", "heavy metal", "death metal", "black metal", "nu metal", "metalcore", "thrash metal"],
    "🌿 Indie & Alternativo": ["indie", "indie rock", "indie pop", "alternative", "alternative rock", "shoegaze", "post-punk", "new wave"],
    "🏕️ Country & Folk": ["country", "folk", "americana", "bluegrass", "singer-songwriter", "acoustic"],
    
    # --- CHILL, SOUL Y RELAJACIÓN ---
    "🎷 Soul & R&B": ["rnb", "r&b", "soul", "funk", "neo soul", "motown", "rhythm and blues"],
    "☁️ Chill & Lo-Fi": ["lo-fi", "chill", "chillout", "ambient", "downtempo", "relax", "bedroom pop"],
    "☕ Jazz & Blues": ["jazz", "blues", "smooth jazz", "bossa nova", "vocal jazz", "swing"],
    
    # --- CONCENTRACIÓN Y ESTUDIO ---
    "🎻 Clásica & Instrumental": ["classical", "instrumental", "soundtrack", "piano", "orchestral", "composer", "easy listening", "soft rock"]
}
def calcularVibra(listaTextosGeneros):
    puntuacion = {vibra: 0 for vibra in diccionarioVibras.keys()}
    for texto in listaTextosGeneros:
        if texto not in ["sin clasificar","no encontrado"]:
            etiquetasIndividuales = [tag.strip() for tag in texto.split(",")]
            #se reparten los puntos
            for tag in etiquetasIndividuales:
                for vibra, palabrasClave in diccionarioVibras.items():
                    if tag in palabrasClave:
                        puntuacion[vibra]+=1
                        #break #si ya encontró la categoría, pasa a la siguiente etiqueta
    #vibra ganadora
    vibraGanadora = max(puntuacion, key=puntuacion.get)
    #vibra neutral
    if puntuacion[vibraGanadora] == 0:
        return "Variado"
    
    return vibraGanadora

feelingMensual["vibraDominante"] = feelingMensual["generos"].apply(calcularVibra)
resumenFeeling = feelingMensual[["mesReproduccion","vibraDominante"]]

# --- MENÚ INTERACTIVO EN CONSOLA ---
while True:
    print("1. Tiempo de escucha mensual")
    print("2. Top 5 Artistas por mes")
    print("3. Top 5 Canciones por mes")
    print("4. Resumen Semanal")
    print("5. Feeling / Vibra Mensual")
    print("6. Salir")
    
    opcion = input("\nElige una opción (1-6): ")
    
    match opcion:
        case "1":
            print("\n--- TIEMPO DE ESCUCHA MENSUAL ---")
            print(tabulate(dfTiempoMensual, headers='keys', tablefmt='psql', showindex=False))
        case "2":
            print("\n--- TOP 5 ARTISTAS POR MES ---")
            print(tabulate(top5Artistas, headers='keys', tablefmt='psql', showindex=False))
        case "3":
            print("\n--- TOP 5 CANCIONES POR MES ---")
            print(tabulate(top5Canciones, headers='keys', tablefmt='psql', showindex=False))
        case "4":
            print("\n--- RESUMEN SEMANAL ---")
            print(tabulate(resumenSemanal, headers='keys', tablefmt='psql', showindex=False, maxcolwidths=35))
        case "5":
            print("\n--- FEELING / VIBRA MENSUAL ---")
            print(tabulate(resumenFeeling, headers='keys', tablefmt='psql', showindex=False))
        case "6":
            print("\nSaliendo del programa")
            break
        case _:
            print("\nOpción no válida")