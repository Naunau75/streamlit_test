import streamlit as st
import requests

st.title("Recherche de Discographie")

artist = st.text_input("Entrez le nom d'un artiste ou d'un groupe :")

if st.button("Rechercher"):
    if artist:
        response = requests.get(f"http://localhost:8000/discography/{artist}")
        if response.status_code == 200:
            data = response.json()
            if "discography" in data:
                st.subheader(f"Discographie de {artist}")
                for release in data["discography"]:
                    st.write(
                        f"{release['year']} - {release['title']} ({release['type']})"
                    )
            else:
                st.error(data.get("error", "Une erreur s'est produite"))
        else:
            st.error("Erreur lors de la communication avec l'API")
    else:
        st.warning("Veuillez entrer un nom d'artiste ou de groupe")
