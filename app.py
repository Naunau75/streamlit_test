import streamlit as st
import requests

st.title("Recherche de Discographie")

artiste = st.text_input("Entrez le nom d'un artiste ou d'un groupe :")

if st.button("Rechercher"):
    if artiste:
        reponse = requests.get(f"http://localhost:8000/discography/{artiste}")
        if reponse.status_code == 200:
            donnees = reponse.json()
            if "discographie" in donnees:
                st.subheader(f"Discographie de {artiste}")
                for sortie in donnees["discographie"]:
                    st.write(
                        f"{sortie['annee']} - {sortie['titre']} ({sortie['type']})"
                    )
            else:
                st.error(donnees.get("erreur", "Une erreur s'est produite"))
        else:
            st.error("Erreur lors de la communication avec l'API")
    else:
        st.warning("Veuillez entrer un nom d'artiste ou de groupe")
