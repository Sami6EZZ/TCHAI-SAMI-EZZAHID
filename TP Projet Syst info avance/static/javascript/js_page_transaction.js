nom_expediteur = localStorage.getItem('nom_utilisateur')
document.getElementById('expediteur').value = "Expéditeur : " + nom_expediteur;

function recupererSolde(nom_expediteur){

    const nom = {'expediteur' : nom_expediteur};

    fetch('/recuperer_solde', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nom)
    })
    .then(response => response.json())
    .then(data => {
            const solde_id = document.getElementById('solde');
            solde_id.textContent = data.solde.toFixed(2);
        })
    .catch(error => {
        console.error('Erreur lors de la requête pour le solde :', error);
    })
}

function enregistrerTransaction() {
    event.preventDefault();
    document.body.style.cursor = "progress";
    var expediteur = localStorage.getItem('nom_utilisateur');
    var recepteur = document.getElementById('recepteur').value;
    var montantInput = document.getElementById('montant');
    var montant = parseFloat(montantInput.value).toFixed(2);
   
    // Construire l'objet avec les données à envoyer
    var transactionData = {
        expediteur: expediteur,
        recepteur: recepteur,
        montant: montant
        };

    // Effectuer la requête HTTP POST
    fetch('/enregistrer_transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(transactionData)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Renvoie la réponse JSON pour la prochaine étape
        } else {
            throw new Error('Erreur ! Veuillez vérifier les données saisies');
        }
    })
    .then(data => {
        // Si la réponse est correcte, afficher le pop-up de succès
        console.log('Réponse de l\'API :', data);
        afficherPopup('Transaction validée', 'success');
    })
    .catch(error => {
        // En cas d'erreur, afficher le pop-up d'erreur
        console.error('Erreur lors de la requête :', error);
        afficherPopup('Erreur lors de la requête', 'error');
    })
    document.body.style.cursor = "default";

    }
function afficherPopup(message, type) {
    Swal.fire({
        title: message,
        icon: type,
        showConfirmButton: false,
        timer: 3000
    }).then(() => {
        location.reload(); // Actualiser la page
    });
}
function afficherHistorique() {
    window.location.href ="page_historique";

}
// Mettez à jour le solde lors du chargement initial de la page
document.addEventListener('DOMContentLoaded', function () {
    recupererSolde(nom_expediteur);
});