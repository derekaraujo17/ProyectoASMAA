import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pylast
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()

#credenciales de spotify
clientId = os.getenv("SPOTIFY_CLIENT_ID")
clientSecret = os.getenv("SPOTIFY_CLIENT_SECRET")
credenciales = SpotifyClientCredentials(client_id=clientId,client_secret=clientSecret)
sp = spotipy.Spotify(auth_manager=credenciales)

#credenciales de last.fm
apiKey = os.getenv("LASTFM_API_KEY")
apiSecret = os.getenv("LASTFM_API_SECRET")
network = pylast.LastFMNetwork(api_key=apiKey, api_secret=apiSecret)

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
        return "🔀 Variado"
    
    return vibraGanadora

#MÓDULO 1: "Historial completo". Utiliza datos json

def procesarDatosJson(archivosSubidos):
    listadf = []
    mesesEspañol = {
        1:"Enero", 2:"Febrero", 3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
        7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"
    }
    for archivo in archivosSubidos:
        dfTemporal = pd.read_json(archivo)
        listadf.append(dfTemporal)
    dfSpotify = pd.concat(listadf, ignore_index=True)

    #limpieza de canciones que no sirven
    umbralMs = 30000 #umbral de tiempo mínimo de reproducción
    filasAntes = len(dfSpotify)
    dfLimpio = dfSpotify[dfSpotify["msPlayed"]>=umbralMs]
    filasDespues = len(dfLimpio)

    #se hace una copia del df para no modificar el original
    dfLimpio = dfLimpio.copy()
    #creación de columnas dentro de este df copia para obtener mes, día y hora de reproducción, usando la columna "endTime" como referencia
    dfLimpio["endTime"] = pd.to_datetime(dfLimpio["endTime"])
    mes = dfLimpio["endTime"].dt.month.map(mesesEspañol)
    año = dfLimpio["endTime"].dt.year.astype(str)
    dfLimpio["añoMesReproduccion"] = (mes + " " + año) 
    dfLimpio["semanaReproduccion"] = dfLimpio["endTime"].dt.strftime('%Y-%V')
    dfLimpio["msPlayed"] = dfLimpio["msPlayed"]/60000
    dfLimpio = dfLimpio.rename(columns={"msPlayed":"minutosReproducidos"})
    dfLimpio["minutosReproducidos"]=dfLimpio["minutosReproducidos"].round(0).astype(int)

    #TIEMPO DE ESCUCHA MENSUAL
    #agrupación por mes de reproducción y suma del tiempo de reproducción, obteniendo así el total de escucha por mes
    dfTiempoMensual = dfLimpio.groupby("añoMesReproduccion")["minutosReproducidos"].sum().reset_index() #esto regresa una serie donde el índice será el mes, y el valor es la suma de los ms
    #promedio de tiempo por mes
    maximoMinutos = dfTiempoMensual["minutosReproducidos"].max()
    dfTiempoMensual["porcentajeReloj"] = dfTiempoMensual["minutosReproducidos"]/maximoMinutos
    
    #ARTISTAS MÁS ESCUCHADOS
    #agrupación por artistas más escuchados
    dfArtistasMensual = dfLimpio.groupby(["añoMesReproduccion","artistName"])["minutosReproducidos"].sum().reset_index()
    dfArtistasMensual =dfArtistasMensual.sort_values(by=["añoMesReproduccion","minutosReproducidos"],ascending=[True,False])
    top5Artistas =dfArtistasMensual.groupby("añoMesReproduccion").head()

    #CANCIONES MÁS ESCUCHADAS
    dfCancionesMensual = dfLimpio.groupby(["añoMesReproduccion","trackName","artistName"]).agg(
        totalMinutos = ("minutosReproducidos","sum"),
        cantidadEscuchas = ("trackName","count")
    ).reset_index()
    dfCancionesMensual=dfCancionesMensual.sort_values(by=["añoMesReproduccion","totalMinutos"],ascending=[True,False])
    top5Canciones=dfCancionesMensual.groupby("añoMesReproduccion").head()

    #RESUMEN SEMANAL
    dfCancionesSemanal = dfLimpio.groupby(["semanaReproduccion","trackName","artistName"]).agg(
        totalMinutos = ("minutosReproducidos","sum"),
        cantidadEscuchas = ("trackName","count")
    ).reset_index()
    dfCancionesSemanal = dfCancionesSemanal.sort_values(by=["semanaReproduccion","totalMinutos"],ascending=[True,False])
    resumenSemanal = dfCancionesSemanal.groupby("semanaReproduccion").head()

    #FEELING MENSUAL
    memoriaGeneros={}
    top20CancionesMensual = dfCancionesMensual.groupby("añoMesReproduccion").head(20).copy()
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
    feelingMensual = top20CancionesMensual.groupby("añoMesReproduccion")[["generos"]].agg(list).reset_index()

    feelingMensual["vibraDominante"] = feelingMensual["generos"].apply(calcularVibra)
    feelingMensual["emoji"] = feelingMensual["vibraDominante"].str[0]
    resumenFeeling = feelingMensual[["añoMesReproduccion","vibraDominante","emoji"]]

    #canciones top 1
    cancionesTop1 = top5Canciones.groupby("añoMesReproduccion").head(1).copy()
    cancionesTop1["urlPortada"] = ""
    for indice, fila in cancionesTop1.iterrows():
        artista1 = fila["artistName"]
        cancion1 = fila["trackName"]
        try:
            resultado = sp.search(q=f"track:{cancion1} artist:{artista1}", type="track",limit=1)
            urlPortada = resultado['tracks']['items'][0]['album']['images'][0]['url']
            cancionesTop1.at[indice,"urlPortada"] = urlPortada
        except Exception as e:
            cancionesTop1.at[indice,"urlPortada"] = "sin imagen"
    
    #artistas top 1
    artistasTop1 = top5Artistas.groupby("añoMesReproduccion").head(1).copy()
    artistasTop1["urlFoto"] = ""
    for indice, fila in artistasTop1.iterrows():
        artista1 = fila["artistName"]
        try:
            resultado = sp.search(q=f"artist:{artista1}", type="artist",limit=1)
            urlFoto = resultado['artists']['items'][0]['images'][0]['url']
            artistasTop1.at[indice,"urlFoto"] = urlFoto
        except Exception as e:
            artistasTop1.at[indice,"urlFoto"] = "sin imagen"

    return dfTiempoMensual, top5Artistas, top5Canciones, resumenSemanal, resumenFeeling, cancionesTop1, artistasTop1