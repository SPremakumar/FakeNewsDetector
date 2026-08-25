import webbrowser
import threading
import time
import os
import sys

# Chemin vers le dossier backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
sys.path.insert(0, BACKEND_DIR)

from app import app


def ouvrir_navigateur():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    # Ouvre le navigateur après le démarrage du serveur
    threading.Thread(target=ouvrir_navigateur, daemon=True).start()
    # Démarrage de Flask
    app.run(host="127.0.0.1", port=5000, debug=False)