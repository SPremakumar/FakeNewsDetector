// URL de l'API Flask
const API_URL = 'https://fakenewsdetector-3dbh.onrender.com';

// Gère la communication avec le backend Flask
export const sendPrediction = async (texte) => {

  try {

    // Vérification du contenu
    if (typeof texte !== 'string') {
      throw new Error(
        'Le texte envoyé doit être une chaîne de caractères.'
      );
    }

    // Vérification du texte vide
    if (!texte.trim()) {
      throw new Error(
        'Le texte à analyser ne peut pas être vide.'
      );
    }

    // Envoie le texte à l'API Flask
    const response = await fetch(`${API_URL}/api/predict`, {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify({
        texte,
      }),
    });

    // Gestion des erreurs HTTP
    if (!response.ok) {

      let message = `Erreur HTTP ${response.status}`;

      // Essaie de récupérer le message d'erreur envoyé par Flask
      try {
        const errorData = await response.json();

        if (errorData.message) {
          message = errorData.message;
        }

      } catch {
        // La réponse n'est pas du JSON
      }

      throw new Error(message);
    }

    // Récupère la réponse JSON de Flask
    const data = await response.json();

    // Vérifie que le serveur a retourné des données
    if (!data) {
      throw new Error(
        'Le serveur a retourné une réponse vide.'
      );
    }

    // Retourne les données à App.jsx
    return data;

  } catch (error) {

    // Serveur inaccessible / problème réseau
    if (error instanceof TypeError) {

      console.error(
        'Impossible de contacter le serveur Flask.'
      );

      throw new Error(
        'Le serveur Flask est inaccessible. Vérifiez qu’il est démarré.'
      );
    }

    console.error(
      'Erreur lors de la communication avec Flask :',
      error
    );

    throw error;
  }
};