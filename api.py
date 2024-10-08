from fastapi import FastAPI
import discogs_client
from config import DISCOGS_API_KEY, DISCOGS_API_SECRET

app = FastAPI()

# Initialisez le client Discogs avec votre clé API et votre secret
d = discogs_client.Client(
    "VotreAppDiscogs/1.0",
    consumer_key=DISCOGS_API_KEY,
    consumer_secret=DISCOGS_API_SECRET,
)


@app.get("/discography/{artist}")
async def get_discography(artist: str):
    try:
        results = d.search(artist, type="artist")
        if results:
            artist_id = results[0].id
            artist_obj = d.artist(artist_id)
            releases = artist_obj.releases
            discography = [
                {"title": release.title, "year": release.year, "type": release.type}
                for release in releases
            ]
            return {"discography": discography}
        else:
            return {"error": "Artiste non trouvé"}
    except Exception as e:
        return {"error": str(e)}
