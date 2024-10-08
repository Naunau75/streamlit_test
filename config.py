import configparser
import os

# Chemin vers le fichier config.ini
CONFIG_FILE = "config.ini"

# Vérifier si le fichier config.ini existe
if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"Le fichier {CONFIG_FILE} n'a pas été trouvé.")

# Créer un objet ConfigParser
config = configparser.ConfigParser()

# Lire le fichier config.ini
config.read(CONFIG_FILE)

# Récupérer les valeurs de la section DISCOGS
DISCOGS_API_KEY = config.get("DISCOGS", "DISCOGS_API_KEY")
DISCOGS_API_SECRET = config.get("DISCOGS", "DISCOGS_API_SECRET")
DISCOGS_USER_TOKEN = config.get("DISCOGS", "DISCOGS_USER_TOKEN")
