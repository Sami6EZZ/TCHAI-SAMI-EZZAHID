import os
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
from flask_bcrypt import Bcrypt

from SQLite_bdd import creer_base_de_donnees
from UAPI_blueprint.F_pages_web import navigation
from UAPI_blueprint.F_inscription import route_inscription
from UAPI_blueprint.F_connexion import route_connexion
from UAPI_blueprint.F_transaction import route_transaction
from UAPI_blueprint.F_historique import route_historique
from UAPI_blueprint.F_solde import route_solde
from UAPI_blueprint.F_historique_user import route_filtre



app = Flask(__name__)

creer_base_de_donnees()

# Récupérer la clé secrète à partir de la variable d'environnement MY_SECRET_KEY
CLE_ID = os.environ.get("CLE_ID", "CLE_ID")

# Vérifier si la clé secrète est définie
if CLE_ID is None:
    raise ValueError("La clé secrète n'est pas définie dans les variables d'environnement.")

# Enregistrer la clé secrète dans l'objet app.config
app.config['CLE_ID'] = CLE_ID
app.secret_key = CLE_ID

transactions = []

# Les routes Flask de l'application
app.register_blueprint(navigation)

app.register_blueprint(route_inscription)

app.register_blueprint(route_connexion)

app.register_blueprint(route_transaction)

app.register_blueprint(route_historique)

app.register_blueprint(route_solde)

app.register_blueprint(route_filtre)




if __name__ == '__main__':
    app.run(debug=True)

