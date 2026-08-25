import '../styles/TextInput.css'

const TextInput = ({ texte, setTexte, onAnalyse }) => {
  return (
    <div className="text-input">
      <h2>Entrez votre texte</h2>
      <textarea
        value={texte}
        onChange={(e) => setTexte(e.target.value)}
        placeholder="Écrivez votre information ici..."
        rows="10"
        cols="50"
      />

      <button onClick={onAnalyse}> Analyser</button>
      
    </div>
  );
};

export default TextInput;