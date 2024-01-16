from flask import Blueprint, render_template

navigation = Blueprint("F_pages_web", __name__)

# routes pour se déplacer entre les différentes pages html
@navigation.route('/')
def page_1():
    return render_template("page_connexion.html")

@navigation.route('/page_transaction' )
def page_accueil():
    return render_template("page_transaction.html")

@navigation.route('/page_historique' )
def page_histo():
    return render_template("page_historique.html")
