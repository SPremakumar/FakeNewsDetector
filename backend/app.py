from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import json
import os
import sys

# CHEMINS
# Dossier du projet FakeNewsDetector
if getattr(sys, "frozen", False):
    PROJECT_DIR = sys._MEIPASS
else:
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BACKEND_DIR = os.path.join(PROJECT_DIR, "backend")

app = Flask(__name__)

# Autoriser le frontend Render
CORS(app,
    resources={
        r"/api/*": {
            "origins": [
                "https://fakenewsdetector-frontend-wajf.onrender.com"
            ]
        }
    }
)

# dictionnaire label binaire -> texte.
labels = {
    0: "Vrai déclaration",
    1: "Fausse déclaration"
}

# CHARGEMENT DU MODÈLE
model_path = os.path.join(BACKEND_DIR, "fake_news_model.keras")
model = tf.keras.models.load_model(model_path)
print(">>>>>>>>>> Modèle Keras chargé")  # todebug

# CHARGEMENT DU VOCABULAIRE
vocab_path = os.path.join(BACKEND_DIR, "vocab.json")
with open(vocab_path, "r", encoding="utf-8") as f:
    vocab = json.load(f)
print(">>>>>>>>>> Vocabulaire chargé")  # todebug

# VECTORISER
vectorizer = tf.keras.layers.TextVectorization(max_tokens=10000, output_sequence_length=30)
vectorizer.set_vocabulary(vocab)
print(">>>>>>>>>> Vectorizer chargé")  # todebug


@app.route("/api/predict", methods=["POST"])
def predict():
    # Récupération des données envoyées par React
    data = request.get_json(silent=True)

    # Récupération du texte
    texte = data.get("texte", "")

    # Transformation du texte en séquence
    sequence = vectorizer([texte])

    # Prédiction avec le Bi-LSTM
    print(sequence.shape, flush=True)
    # prediction = model.predict(sequence,verbose=0) # fonctionne pas avec render 
    # print("Prédiction :", prediction)  # todebug
    # prediction = predict(sequence, verbose=0) # fonctionne pas avec render 
    prediction = model(sequence, training=False).numpy()

    # Classe gagnante
    classe = int(np.argmax(prediction[0]))

    # Confiance
    confiance = float(prediction[0][classe])
    print("Confiance :", confiance)  # todebug

    # Résultat
    resultat = labels[classe]
    print("Résultat :", resultat)

    return jsonify({
        "prediction": resultat,
        "confidence": confiance
    })


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "FakeNewsDetector API fonctionne"
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)