import streamlit as st
import requests
import math

st.title("Recherche de Discographie")

# Initialisation de la session state pour la page et les données
if "page" not in st.session_state:
    st.session_state.page = 1
if "discographie" not in st.session_state:
    st.session_state.discographie = None

artiste = st.text_input("Entrez le nom d'un artiste ou d'un groupe :")

if st.button("Rechercher") or st.session_state.discographie:
    if artiste or st.session_state.discographie:
        if not st.session_state.discographie:
            reponse = requests.get(f"http://localhost:8000/discography/{artiste}")
            if reponse.status_code == 200:
                donnees = reponse.json()
                if "discographie" in donnees:
                    st.session_state.discographie = donnees["discographie"]
                else:
                    st.error(donnees.get("erreur", "Une erreur s'est produite"))
                    st.session_state.discographie = None
            else:
                st.error("Erreur lors de la communication avec l'API")
                st.session_state.discographie = None

        if st.session_state.discographie:
            st.subheader(f"Discographie de {artiste}")

            # Pagination
            resultats_par_page = 25
            total_resultats = len(st.session_state.discographie)
            total_pages = math.ceil(total_resultats / resultats_par_page)

            st.session_state.page = st.number_input(
                "Page", min_value=1, max_value=total_pages, value=st.session_state.page
            )
            debut = (st.session_state.page - 1) * resultats_par_page
            fin = debut + resultats_par_page

            for sortie in st.session_state.discographie[debut:fin]:
                st.write(f"{sortie['annee']} - {sortie['titre']} ({sortie['type']})")

            st.write(f"Page {st.session_state.page} sur {total_pages}")

            # Boutons de navigation
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Page précédente", disabled=(st.session_state.page == 1)):
                    st.session_state.page -= 1
                    st.rerun()
            with col2:
                if st.button(
                    "Page suivante", disabled=(st.session_state.page == total_pages)
                ):
                    st.session_state.page += 1
                    st.rerun()
    else:
        st.warning("Veuillez entrer un nom d'artiste ou de groupe")
