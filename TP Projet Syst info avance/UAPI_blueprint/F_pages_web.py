from flask import Blueprint, render_template

navigation = Blueprint("F_pages_web", __name__)

# routes pour se déplacer entre les différentes pages html
@navigation.route('/')
def page_1():
    return render_template("page_connexion.html")

@navigation.route('/page_accueil' )
def page_accueil():
    return render_template("page_accueil.html")
