# FakeNewsDetector

FakeNewsDetector est une application de détection de fausses informations basée sur l'intelligence artificielle.

L'application permet à l'utilisateur de saisir une information textuelle et d'obtenir une prédiction indiquant si celle-ci est considérée comme vraie ou fausse, accompagnée d'un score de confiance.


## Application web

L’application est disponible en ligne et peut être utilisée directement depuis un navigateur :

"Accéder à la WebApp FakeNewsDetector" (https://fakenewsdetector-frontend-wajf.onrender.com/)

La WebApp permet de saisir une information et d’obtenir une prédiction indiquant si elle est considérée comme vraie ou fausse, avec un niveau de confiance associé.

## Utilisation

### Version Windows

Pour utiliser FakeNewsDetector sans installer Python ni les dépendances :

1. Télécharger `FakeNewsDetector-Windows-v1.0.0.zip` depuis la section **Releases**.
2. Extraire le fichier ZIP.
3. Double-cliquer sur `FakeNewsDetector.exe`.
4. Attendre le démarrage de l'application. Le premier lancement peut prendre environ une minute.
5. Le navigateur s'ouvre automatiquement sur l'application.

### Effectuer une prédiction

Une fois l'application ouverte :

1. Saisir une information ou une affirmation dans la zone de texte.
2. Cliquer sur le bouton **Envoyer**.
3. L'application transmet le texte au serveur Flask.
4. Le texte est transformé en séquence numérique grâce au vocabulaire utilisé lors de l'entraînement.
5. Le modèle **Bi-LSTM** analyse le texte.
6. Le résultat est affiché dans l'interface.

Le résultat indique :

- **true statement** : l'information est classée comme vraie par le modèle.
- **false statement** : l'information est classée comme fausse par le modèle.
- **Confiance** : probabilité associée à la classe prédite.

### Exemple

Texte saisi :

```text
Donald Trump is the president now.
```

## Fonctionnalités

- Détection de fausses informations
- Modèle de classification **Bi-LSTM**
- Vectorisation des textes avec `TextVectorization`
- Interface utilisateur développée avec **React**
- API développée avec **Flask**
- Score de confiance de la prédiction
- Application Windows autonome au format `.exe`
- Ouverture automatique de l'application dans le navigateur

## Technologies utilisées

### Frontend

- React
- Vite
- JavaScript
- HTML
- CSS

### Backend

- Python
- Flask
- Flask-CORS
- TensorFlow
- Keras
- NumPy

### Modèle

Le modèle utilisé est un réseau de neurones **Bidirectional LSTM (Bi-LSTM)**.

Le pipeline de prédiction est le suivant :

```text
Texte utilisateur
       ↓
TextVectorization
       ↓
Séquence d'entiers
       ↓
Bi-LSTM
       ↓
Softmax
       ↓
Classe prédite
       ↓
Confiance```

