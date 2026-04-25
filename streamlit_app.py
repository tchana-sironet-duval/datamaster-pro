import streamlit as st

st.title("Application de collecte de données")

nom = st.text_input("Nom")
age = st.number_input("Age")

if st.button("Envoyer"):
    st.success("Données enregistrées")
