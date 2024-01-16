// Supposons que vous avez déjà une liste d'objets transactions
let transactions = [];

const transactionsList = document.querySelector('.transactions-list');
const filterSpan = document.getElementById('filter');
const utilisateurInput = document.getElementById('utilisateurInput');

// Fonction pour afficher la liste des transactions
function afficherTransactions(transaction) {
    const tbody = document.querySelector('.transactions-list tbody');
    tbody.innerHTML = ''; // Efface le contenu actuel du tbody

    transaction.forEach(transaction => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${transaction.date_heure}</td>
                        <td>${transaction.expediteur}</td>
                        <td>${transaction.recepteur}</td>
                        <td>${transaction.montant} €</td>`;
        tbody.appendChild(row);
    });
}

// Fonction pour charger les transactions depuis le serveur (ajuster l'URL selon votre configuration)
function chargerTransactions() {
    fetch('/charger_transactions')
        .then(response => response.json())
        .then(data => {
            transactions = data.transactions; // Assurez-vous d'adapter la structure de la réponse
            afficherTransactions(transactions);
        })
        .catch(error => {
            console.error('Erreur lors du chargement des transactions :', error);
        });
}

// Mettez à jour la liste des transactions lors du chargement initial de la page
document.addEventListener('DOMContentLoaded', function () {
    chargerTransactions();
});



// Fonction pour afficher le message d'erreur
function afficherMessageErreur(message) {
    const erreurUtilisateur = document.getElementById('erreur-utilisateur');
    erreurUtilisateur.textContent = message;
}

// Fonction pour afficher l'historique filtré
function afficherHistoriqueFiltre(utilisateur) {
    filterSpan.textContent = utilisateur === '' ? 'Tout' : utilisateur;

    if (utilisateur === '' || utilisateur.toLowerCase() === 'tout' || utilisateur === null) {

        chargerTransactions();
        afficherMessageErreur('');
    } else {
        fetch(`/verifier_utilisateur?utilisateur=${utilisateur}`)
            .then(response => response.json())
            .then(data => {
                if (data.utilisateurExiste) {
                    fetch(`/charger_transactions_utilisateur?utilisateur=${utilisateur}`)
                        .then(response => response.json())
                        .then(data => {
                            afficherTransactions(data.transactions);
                            afficherMessageErreur('');
                        })
                        .catch(error => console.error('Erreur lors du chargement des transactions :', error));
                } else {
                    afficherMessageErreur('Utilisateur incorrect. Veuillez réessayer.');
                }
            })
            .catch(error => console.error('Erreur lors de la vérification de l\'utilisateur :', error));
    }
}

// Écoutez les changements dans l'input utilisateur
utilisateurInput.addEventListener('change', function (event) {
    const utilisateur = this.value.trim();
    afficherHistoriqueFiltre(utilisateur);
});


// fonction de vérification des transactions
function verifierTransactions() {
    fetch('/verifier_transactions')
        .then(response => response.json())
        .then(data => {
            const transactionsFrauduleusesDiv = document.getElementById('transactions-frauduleuses');
            const listeTransactionsFrauduleusesDiv = document.getElementById('liste-transactions-frauduleuses');

            // Afficher ou masquer l'élément selon la présence de transactions frauduleuses
            transactionsFrauduleusesDiv.style.display = data.transactions_frauduleuses.length > 0 ? 'block' : 'none';

            if (data.transactions_frauduleuses.length === 0) {
                // Transactions validées
                afficherPopup('Transactions validées', 'success');
            } else {
                // Transactions frauduleuses détectées
                afficherPopup('Transactions frauduleuses détectées', 'error');
                // Afficher la liste des transactions frauduleuses
                listeTransactionsFrauduleusesDiv.textContent = data.transactions_frauduleuses.map(transaction => JSON.stringify(transaction)).join('\n');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la vérification des transactions :', error);
        });
}
function afficherPopup(message, type) {
    Swal.fire({
        title: message,
        icon: type,
        showConfirmButton: false,
        timer: 3000
    });
}