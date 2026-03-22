import streamlit as st

def mostrar_pantalla_botones():
    st.title("Elegir la opción de los datos")

    col1, col2 = st.columns(2)

    with col1:
        #botón json
        if st.button("JSON"):
            st.session_state["pantalla_actual"] = "dashboardjson"
            st.rerun()
    with col2:
        #botón oauth
        if st.button("OAuth"):
            st.session_state["pantalla_actual"] = "dashboardouath"
            st.rerun()