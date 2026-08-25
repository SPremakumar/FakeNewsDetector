import '../styles/OutputPreview.css'


const LivePreview = ({ resultat, confiance }) => {

  // Composant pour la prévisualisation de latex 
  return (
    <div className="live-preview">
      <h2 className="preview-title">Résultat</h2>
      <div className="preview-content">
      	{!resultat ? (
          <p>Aucun résultat pour le moment...</p>
        ) : (
          <>
            <h3>{resultat}</h3>
	        {/* Indice de confiance toujours affiché */}
	        <p>
	          Confiance : {
	            confiance !== null && confiance !== undefined
	              ? (confiance * 100).toFixed(2)
	              : "0.00"
	          } %
	        </p> 
          </>
        )}
      </div>
    </div>
  );
};

export default LivePreview;