import os
from flask import send_file, current_app
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, request, url_for, flash, redirect
import uuid
from werkzeug.utils import secure_filename
from flask_login import current_user
from plugins.services.requestnote_v0_0.models import *
from plugins.services.requestnote_v0_0.schemas import *
from plugins.services.requestnote_v0_0.forms import *
from datetime import datetime
from sqlalchemy import desc
from io import BytesIO
from marshmallow import ValidationError
# from app import app
from flask_mail import Mail, Message
from core.utils import (
    UiBlueprint, 
    read_json, 
    read_markdown, 
    paginate_items, 
    default_deadline,
    get_locale
)

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = 'prodistributionltd237@gmail.com'
# app.config['MAIL_PASSWORD'] = 'dovm cgou tqpn yldu'
# app.config['MAIL_DEFAULT_SENDER'] = 'prodistributionltd237@gmail.com'


mail = Mail()

ui = UiBlueprint(__name__)

ui.register_entry('home_menu', 'home_demo4', _l('requete'), endpoint='requestnote.index', rank=4)

upload_folder = 'plugins/pages/requestnote/static/uploads'
os.makedirs(upload_folder, exist_ok=True)

# student request :: route a changer
@ui.login_required
@ui.route("/")
def index():
    requetes = Requete.query.filter_by(etudiant_id=current_user.id).order_by(Requete.date_engr.desc()).all()
    suspendu = Requete.query.filter_by(status="suspendu").order_by(Requete.date_engr.desc()).all()
    rejeter = Requete.query.filter_by(status="rejeter").order_by(Requete.date_engr.desc()).all()
    terminer = Requete.query.filter_by(status="terminer").order_by(Requete.date_engr.desc()).all()
    debut = Requete.query.filter_by(status="en attente").order_by(Requete.date_engr.desc()).all()
    return render_template("index.jinja", requetes=requetes, suspendu=suspendu, rejeter=rejeter, terminer=terminer, debut=debut)

@ui.login_required
@ui.route("/soumettre-une-requete", methods=['GET', 'POST'])
def send_requete():
    requetes = Requete.query.filter_by(etudiant_id=current_user.id).order_by(Requete.date_engr.desc()).all()
    # form = RequeteForm()
    teachers = Responsable.query.all()
    if request.method == "POST": 
        schema = RequestSchema()
        # tr/y:
        data = request.form.to_dict()
        # data['etudiant_id'] = current_user.id
            # Valider les données du formulaire
        data = schema.load(request.form)

            # Gérer le fichier
        piece = request.files.get('piece')
        filename = None
        if piece and piece.filename:
            ext = os.path.splitext(piece.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(upload_folder, filename)
            
            # Assure-toi que le dossier existe
            os.makedirs(upload_folder, exist_ok=True)
            piece.save(file_path)
            # file_path = os.path.join(upload_folder, filename)
            # piece.save(file_path)
        # print(piece)
            # Enregistrement en base
        requete = Requete(
                objet=data.objet,
                intitule_ec=data.intitule_ec,
                description=data.description,
                responsable_id=data.responsable_id,
                piece=filename,
                etudiant_id=current_user.id
            )
        db.session.add(requete)
        db.session.commit()

        responsable = Responsable.query.get(data.responsable_id)
        url = "http://127.0.0.1:5000/requestnote/"

        msg = Message(
            subject="Nouvelle requête à traiter",
            recipients=[responsable.email],  # ou une adresse par défaut pour tester
            # body=f"Bonjour {responsable.nom},\n\nUne nouvelle requête vous a été adressée.",
            html=render_template('emails/new-requete.jinja',requete=requete, responsable=responsable, url=url)
        )
        mail.send(msg)

        flash("Requête déposée avec succès", "success")
        return redirect(url_for("requestnote.index"))

        # except ValidationError as err:
            # flash(f"Erreur de validation : {err.messages}", "danger")
  
    
    return render_template("send-requete.jinja",teachers=teachers, requetes=requetes)

@ui.login_required
@ui.route('/ouvrir/<int:id>')
def ouvrir_fichier(id):
    # Récupérer le fichier depuis la base de données
    requete = Requete.query.get_or_404(id)
    
    # Créer un objet fichier en mémoire
    chemin = os.path.join('..','plugins', 'pages', 'requestnote', 'static', 'uploads', requete.piece)
    # chemin = os.path.join(upload_folder, requete.piece)
    # print(chemin)
    
    # Envoyer le fichier au client pour affichage
    return send_file(
        chemin,
        as_attachment=False,  # False pour ouvrir dans le navigateur
        download_name=requete.piece  # Nom suggéré si téléchargement manuel
    )

@ui.login_required
@ui.route('/open/<int:id>')
def ouvrir_file(id):
    # Récupérer le fichier depuis la base de données
    justificatif = Justificatif.query.get_or_404(id)
    # Créer un objet fichier en mémoire
    chemin = os.path.join('..','plugins', 'pages', 'requestnote', 'static', 'uploads', justificatif.justificatif)
    # chemin = os.path.join(upload_folder, requete.piece)
    # print(chemin)
    # Envoyer le fichier au client pour affichage
    return send_file(
        chemin,
        as_attachment=False,  # False pour ouvrir dans le navigateur
        download_name=justificatif.justificatif  # Nom suggéré si téléchargement manuel
    )

@ui.login_required
@ui.route("/detail-de-la-requete/<int:id>/",methods=['GET', 'POST'])
def get_detail(id):
    requetes = Requete.query.filter_by(etudiant_id=current_user.id).order_by(Requete.date_engr.desc()).all()
    requetep = Requete.query.get_or_404(id)
    justificatifs = Justificatif.query.filter_by(requete_id=id).all()
    responsablee= Responsable.query.get_or_404(requetep.responsable_id)
    if request.method == 'POST':
        schema= JustificatifSchema()
        data = request.form.to_dict()
        data = schema.load(request.form)

        piece = request.files.get('justificatif')
        filename = None
        if piece and piece.filename:
            ext = os.path.splitext(piece.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(upload_folder, filename)
            
            # Assure-toi que le dossier existe
            os.makedirs(upload_folder, exist_ok=True)
            piece.save(file_path)
    
            requete = Justificatif(
                justificatif=filename,
                requete_id=data.requete_id,
                libelle=data.libelle,
            )
            db.session.add(requete)
            db.session.commit()
            
            flash("Justificatif ajouter avec succès", "success")
            # data=""
            return redirect(url_for('requestnote.get_detail', id=requetep.id))
            # return render_template("detail-requete.jinja", requetes=requetes, requete=requetep, justificatifs=justificatifs, responsable=responsablee)
    else :     
        return render_template("detail-requete.jinja", requetes=requetes, requete=requetep, justificatifs=justificatifs, responsable=responsablee)

@ui.login_required
@ui.route("/requete-adresse")
def get_reponsable():
    return render_template("responsable-page.jinja")