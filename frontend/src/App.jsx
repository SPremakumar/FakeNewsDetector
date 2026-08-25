import { useState } from 'react'
import TextInput from "./components/TextInput";
import LivePreview from "./components/OutputPreview";
import { sendPrediction } from "./components/BackEndConnection";
import './App.css'

function App() {
  const [texte, setTexte] = useState("");
  const [resultat, setResultat] = useState("");
  const [confiance, setConfiance] = useState(null);


  // Envoie le texte à Flask et récupère la prédiction du modèle
  const analyser = async () => {
    try {
      const data = await sendPrediction(texte);
      setResultat(data.prediction);
      setConfiance(data.confidence);
    } catch (error) {
      console.error(error);
    }
  };


  return (
    <div className="app">
      <h1>Détecteur de fausse information</h1>

      <div className="editor-layout">
        <TextInput texte={texte} setTexte={setTexte} onAnalyse={analyser}/>
        <LivePreview resultat={resultat} confiance={confiance}/>
      </div>


    </div>
  )
}

export default App
