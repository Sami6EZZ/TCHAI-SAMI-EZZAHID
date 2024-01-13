function enregistrerTransaction() {
    var expediteur = document.getElementById('expediteur').value;
    var recepteur = document.getElementById('recepteur').value;
    var monant = document.getElementById('montant').value;
    // Obtenir la date et l'heure actuelles
    var dateTransaction = new Date();
    var dateFormatted = dateTransaction.toISOString(); // Format ISO pour la date et l'heure

    // Construire l'objet avec les données à envoyer
    var transactionData = {
        expediteur: expediteur,
        recepteur: recepteur,
        montant: parseFloat(montant),
        timestamp: dateFormatted
    };

    // Effectuer la requête HTTP POST
    fetch('/enregistrer_transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(transactionData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Réponse de l\'API :', data);
        // Gérer la réponse de l'API ici, si nécessaire
    })
    .catch(error => {
        console.error('Erreur lors de la requête :', error);
        // Gérer les erreurs ici, si nécessaire
    });
    }

function afficherHistorique() {
    // Vous pouvez rediriger l'utilisateur vers la page d'historique des transactions.
    // Exemple : window.location.href = '/historique';
}
