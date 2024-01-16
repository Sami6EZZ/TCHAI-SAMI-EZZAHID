//Code JS pour l'annimation du bloc de connexion/inscription ccccccccccciiiiiiiiiiiiiiiiiicccccccccccccccc

function vers_inscr() {
    document.getElementById("curseur_cyan").style.left = "160px";
  document.querySelector(".formulaire_connexion-inscription").style.transform = "translateX(-400px)";

}

function vers_conn() {
    document.getElementById("curseur_cyan").style.left = "0px";
    document.querySelector(".formulaire_connexion-inscription").style.transform = "translateX(0px)";


    
}

//Code JS pour la connexion cccccccccccccccccccccccccccccccccccccccccc

function connexion() {
    // récupération et stockage les données de connexion dans le stockage local 
    var nom_utilisateur = document.getElementById('username').value;
    localStorage.setItem('nom_utilisateur', nom_utilisateur);
    // récupération et stockage du nom d'utilisateur aulieu du nom de la bdd dans le stockage local pour garder le meme code pour le reste du logiciel !!!!!!
    //var nom_bdd = document.getElementById('nom_bdd').value;
    //localStorage.setItem('nom_bdd', nom_utilisateur);
    // forcer la casse des lettres en miniscule pour eviter les bugs au nveau de la bdd
    var mot_de_passe = document.getElementById('password').value;
    //localStorage.setItem('mot_de_passe', mot_de_passe);
    // Nome du hôte de la base de données doit être le même que le nom du service de la BDD
    //const host = "localhost"; //const host = "image_bdd";
    //localStorage.setItem('host', host);

    const conn = {
        'username': nom_utilisateur,
        'mdp': mot_de_passe
    };
    fetch('/connexion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(conn)
       
        })
        .then(response => {
            if (response.ok) {
                return response.json();

            }
            throw new Error('Erreur lors de la connexion.');
        })
        .then(data => {
                    window.location.href ="page_transaction";
                     
        })
        .catch(erreur => {
            console.error(erreur);
            const username_input = document.getElementById("username");
            const password_input = document.getElementById("password");
            //const nom_bdd_input = document.getElementById("nom_bdd");

            username_input.classList.add('erreur');
            password_input.classList.add('erreur');
            //nom_bdd_input.classList.add('error');
            

            

        })

    
}

//fin code js pour la connexion cccccccccccccccccccccccccccccccccccccccccc


// code JS pour s'inscrir iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

function inscription() {
document.body.style.cursor = "progress";
const nom_utilisateur = document.getElementById('username_ins').value;
const mot_de_passe = document.getElementById('password_ins').value.toLowerCase();
// Récupération du nom de la bdd
//const nom_bdd = document.getElementById('nom_bdd').value;
data = {
    'nom_utilisateur' : nom_utilisateur,
    'mot_de_passe': mot_de_passe
};
 // Vérification de la présence de caractères spéciaux dans le nom d'utilisateur
const regex = /[!@#$%^&*(),.?":{}|<>-]/;
if (regex.test(nom_utilisateur)) {
document.body.style.cursor = "default";
ouvrirPopup("Erreur lors de la création du profil utilisateur !<br><br>Le nom d'utilisateur ne doit pas contenir de caractère spécial.", false);
return;
}
fetch('/inscription', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
   
    })
    
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Erreur lors de la création du profil utilisateur !');
    })
    .then(data => {
        
            ouvrirPopup(data.message, true);
            setTimeout(function() {
                fermerPopup();
                vers_conn();
                
            }, 3000);
        
    })
    .catch(erreur => {

        console.error(erreur);
        
        ouvrirPopup(erreur.erreur, false);
        

        
    })
    document.body.style.cursor = "default";
}
function ouvrirPopup(message, actif) {
    
    document.getElementById('popup').style.display = 'block';
    

    if (actif) {
        document.getElementById('message').innerHTML = 'Le compte <u><strong>' + message + '</strong></u> est désormais actif.';

        document.getElementById('popup_inscription').classList.remove('popup-erreur');
        document.getElementById('popup_check_image_2').style.display = 'none';
        document.getElementById('popup_check_image').style.display = 'block';


    } else {     
        document.getElementById('message').innerHTML = message +'<br><br>Ce nom d\'utilisateur est déjà utilisé.' ;
        document.getElementById('popup_check_image_2').style.display = 'block';
        document.getElementById('popup_check_image').style.display = 'none';
        document.getElementById('popup_inscription').classList.add('popup-erreur');
 
    }
}
function fermerPopup() {
    document.getElementById('popup').style.display = 'none';
}

    

// Fermer la boîte de dialogue si on clic  en dehors du cadre de la boite de dialogue
window.addEventListener('click', function(event) {
      var boite_de_dialogue = document.getElementById('popup_inscription');
      var bouton_inscription = document.getElementById('bouton_inscription');

      if (!boite_de_dialogue.contains(event.target) && !bouton_inscription.contains(event.target) ) {
        fermerPopup();
      } 
      });