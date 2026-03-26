import streamlit as st

def mostrar_pantalla_botones():
    st.title("Elegir la opción de los datos")

    col1, col2 = st.columns(2)

    with col1:
        #botón json
        archivosSubidos = st.file_uploader("Sube tus archivos JSON", accept_multiple_files=True, type=["json"])
        def cargarArchivos():
            archivosValidos=[]
            if len(archivosSubidos)>= 1:
                archivosValidos = [archivo for archivo in archivosSubidos if "StreamingHistory_music" in archivo.name]
                if len(archivosValidos)==0:
                    st.write("""Error al subir los archivos""")
            return archivosValidos
        jsonValidos = cargarArchivos()
        if len(jsonValidos)>=1:
            if st.button("Analizar mis archivos"):
                st.session_state["jsonValidos"] = jsonValidos
                st.session_state["pantalla_actual"] = "pantallaCarga"
                st.rerun()
    with col2:
        #botón oauth
        if st.button("OAuth"):
            st.session_state["pantalla_actual"] = "dashboardoauth"
            st.rerun()