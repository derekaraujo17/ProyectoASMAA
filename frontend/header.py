import streamlit as st

def render_header():
    st.markdown("""
    <div class="custom-header">
        <img src="assets/pibble.png" class="logo">
        <span class="title">SpibblePy</span>
    </div>
    """, unsafe_allow_html=True)