from fastapi import FastAPI
import discogs_client
from config import DISCOGS_USER_TOKEN
import logging
import requests

app = FastAPI()

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisez le client Discogs avec votre clé API et votre secret
d = discogs_client.Client(
    "VotreAppDiscogs/1.0 +http://votresite.com", user_token=DISCOGS_USER_TOKEN
)

# Log de l'initialisation du client Discogs
logger.info("Client Discogs initialisé avec succès")


@app.get("/discography/{artist}")
async def get_discography(artist: str):
    try:
        resultats = d.search(artist, type="artist")
        if resultats:
            artiste_id = resultats[0].id
            url = f"https://api.discogs.com/artists/{artiste_id}/releases"
            headers = {"Authorization": f"Discogs token={DISCOGS_USER_TOKEN}"}
            params = {"per_page": 50, "page": 1}
            discographie = []

            while True:
                reponse = requests.get(url, headers=headers, params=params)

                if reponse.status_code == 200:
                    donnees = reponse.json()
                    discographie.extend(
                        [
                            {
                                "titre": sortie["title"],
                                "annee": sortie["year"],
                                "type": sortie["type"],
                            }
                            for sortie in donnees["releases"]
                        ]
                    )
                return {"discographie": discographie}
            else:
                return {"erreur": "Erreur lors de la récupération des sorties"}
        else:
            return {"erreur": "Artiste non trouvé"}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la discographie: {str(e)}")
        return {
            "erreur": "Une erreur s'est produite lors de la récupération de la discographie"
        }
