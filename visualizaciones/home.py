import streamlit as st

def mostrar_pantalla_pibble():
    st.title("Spibblepy")
    st.write("imagen")
    
    if st.button("Limpiar panza"):
        #cambio de memoria
        st.session_state["autenticado"] = True
        st.session_state["pantalla_actual"] = "seleccion"
        #obligamos a la página a recargarse inmediatamente para que el main.py lea la nueva memoria y cambie de pantalla
        #aquí podrían agregar una animación de carga si es necesaria
        st.reurn()
