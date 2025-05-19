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

ui.register_entry('home_menu', 'home_demo4', _l('requete'), endpoint='requestnote.controle_role', rank=4)

upload_folder = 'plugins/pages/requestnote/static/uploads'
os.makedirs(upload_folder, exist_ok=True)

# student request :: route a changer
@ui.route("/")
@ui.login_required
def controle_role():
        if current_user.has_roles('chef_depart'):
            pass
        elif current_user.has_roles('student'):
            return redirect(url_for('requestnote.index'))
        elif current_user.has_roles('cellule') :
            pass
        elif current_user.has_roles('teacher') :
            return redirect(url_for('requestnote.get_teacher'))
        else :
            return "auccun role"


@ui.route("/accueil")
@ui.login_required
def index():
    url='requestnote.get_detail'
    col = 'col-md-4'
    statut = request.args.get('statut')  # Récupère le statut dans l'URL
    requetes = Requete.query.filter_by(etudiant_id=current_user.id)
    nombre = Requete.query.filter_by(etudiant_id=current_user.id).count()
    if statut:
        requetes = requetes.filter_by(status=statut).order_by(Requete.date_engr.desc()).all()
    else :
        requetes = requetes.order_by(Requete.date_engr.desc()).all()
    valider= Requete.query.filter_by(etudiant_id=current_user.id).filter_by(status="valider").order_by(Requete.date_engr.desc()).all()
    suspendu = Requete.query.filter_by(etudiant_id=current_user.id).filter_by(status="suspendu").order_by(Requete.date_engr.desc()).all()
    rejeter = Requete.query.filter_by(etudiant_id=current_user.id).filter_by(status="rejeter").order_by(Requete.date_engr.desc()).all()
    approuver = Requete.query.filter_by(etudiant_id=current_user.id).filter_by(status="approuver").order_by(Requete.date_engr.desc()).all()
    terminer = Requete.query.filter_by(etudiant_id=current_user.id).filter_by(status="terminer").order_by(Requete.date_engr.desc()).all()
    debut = Requete.query.filter_by(etudiant_id=current_user.id).filter_by(status="en attente").order_by(Requete.date_engr.desc()).all()
    return render_template("index.jinja",url=url,valider=valider, col=col,nombre=nombre, requetes=requetes, approuver=approuver, suspendu=suspendu, rejeter=rejeter, terminer=terminer, debut=debut)

@ui.route("/soumettre-une-requete", methods=['GET', 'POST'])
@ui.login_required
def send_requete():
    url='requestnote.get_detail'
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
        
    
        requete_id = Requete.query.order_by(Requete.id.desc()).first()

        traitement = Traitement(
           requete_id=requete_id.id,
           responsable_id=data.responsable_id,
           statut_id=5
        )
        db.session.add(traitement)
        db.session.commit()

        responsable = Responsable.query.get(data.responsable_id)
        urls = f'http://127.0.0.1:5000/requestnote/requete-adresse-detail/{requete_id.id}'

        msg = Message(
            subject="Nouvelle requête à traiter",
            recipients=[responsable.email],  # ou une adresse par défaut pour tester
            # body=f"Bonjour {responsable.nom},\n\nUne nouvelle requête vous a été adressée.",
            html=render_template('emails/new-requete.jinja',requete=requete, responsable=responsable, urls=urls)
        )
        mail.send(msg)

        flash("Requête déposée avec succès", "success")
        return redirect(url_for("requestnote.index"))

        # except ValidationError as err:
            # flash(f"Erreur de validation : {err.messages}", "danger")
  
    
    return render_template("send-requete.jinja",teachers=teachers, requetes=requetes,url=url)

@ui.route('/ouvrir/<int:id>')
@ui.login_required
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

@ui.route('/open/<int:id>')
@ui.login_required
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

@ui.route("/detail-de-la-requete/<int:id>/",methods=['GET', 'POST'])
@ui.login_required
def get_detail(id):
    url='requestnote.get_detail'
    requetes = Requete.query.filter_by(etudiant_id=current_user.id).order_by(Requete.date_engr.desc()).all()
    requetep = Requete.query.get_or_404(id)
    justificatifs = Justificatif.query.filter_by(requete_id=id).all()
    responsablee= Responsable.query.get_or_404(requetep.responsable_id)
    teachers = Responsable.query.all()
    traitements = Traitement.query.filter_by(requete_id=id).order_by(Traitement.id.desc()).all()[1:]
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
        return render_template("detail-requete.jinja",url=url,traitements=traitements, teachers=teachers, requetes=requetes, requete=requetep, justificatifs=justificatifs, responsable=responsablee)

@ui.route('/detail-de-la-requete/delete/<int:id>')
def delete_requete(id):
    requete = Requete.query.get_or_404(id)
    db.session.delete(requete)
    db.session.commit()
    flash('Requête supprimée avec succès.', 'success')
    return redirect(url_for('requestnote.index'))

# responsable
@ui.route("/requete-adresse")
@ui.login_required
def get_teacher():
    url = 'requestnote.get_teacher'
    statut = request.args.get('statut')  # Récupère le statut dans l'URL
    requetes = Requete.query.filter_by(responsable_id=current_user.id)
    nombre = Requete.query.filter_by(responsable_id=current_user.id).count()
    if statut:
        requetes = requetes.filter_by(status=statut).order_by(Requete.date_engr.desc()).all()
    else :
        requetes = requetes.order_by(Requete.date_engr.desc()).all()
    valider= Requete.query.filter_by(responsable_id=current_user.id).filter_by(status="valider").order_by(Requete.date_engr.desc()).all()
    suspendu = Requete.query.filter_by(responsable_id=current_user.id).filter_by(status="suspendu").order_by(Requete.date_engr.desc()).all()
    rejeter = Requete.query.filter_by(responsable_id=current_user.id).filter_by(status="rejeter").order_by(Requete.date_engr.desc()).all()
    approuver = Requete.query.filter_by(responsable_id=current_user.id).filter_by(status="approuver").order_by(Requete.date_engr.desc()).all()
    terminer = Requete.query.filter_by(responsable_id=current_user.id).filter_by(status="terminer").order_by(Requete.date_engr.desc()).all()
    debut = Requete.query.filter_by(responsable_id=current_user.id).filter_by(status="en attente").order_by(Requete.date_engr.desc()).all()
    return render_template("teacher/responsable-page.jinja",url=url,valider=valider, nombre=nombre, requetes=requetes, approuver=approuver, suspendu=suspendu, rejeter=rejeter, terminer=terminer, debut=debut)


@ui.route("/requete-adresse-detail/<int:id>", methods=['POST','GET'])
@ui.login_required
def get_admin_detail(id):
    if request.method == 'POST':
        schema =TraitementSchema()
        data = request.form.to_dict()
        data = schema.load(request.form)
        requete = Requete.query.get_or_404(id)

        
        observation = None
        
        if data.commentaire :
            commentaire = data.commentaire

        requete.status = data.statut_id
        db.session.commit()
        statut = data.statut_id
        commentaire = data.commentaire
        traitement = Traitement(
           requete_id=requete.id,
           responsable_id=current_user.id,
           statut_id=data.statut_id,
           commentaire=commentaire
        )
        db.session.add(traitement)
        db.session.commit()

        student = Etudiant.query.get(requete.etudiant_id)
        urls = f'http://127.0.0.1:5000/requestnote/detail-de-la-requete/{requete.id}'

        msg = Message(
            subject="Suivis de la requete",
            recipients=[student.email],  # ou une adresse par défaut pour tester
            # body=f"Bonjour {responsable.nom},\n\nUne nouvelle requête vous a été adressée.",
            html=render_template('emails/change-statut.jinja',commentaire=commentaire,statut=statut,requete=requete, student=student, urls=urls)
        )
        mail.send(msg)

        flash("Traitement efectuer", "success")
        return redirect(url_for("requestnote.get_teacher"))
    else : 
      url='requestnote.get_admin_detail'
      requetes = Requete.query.filter_by(responsable_id=current_user.id).order_by(Requete.date_engr.desc()).all()
      requetep = Requete.query.get_or_404(id)
      justificatifs = Justificatif.query.filter_by(requete_id=id).all()
      student= Etudiant.query.filter_by(id=requetep.etudiant_id).first()
      traitements = Traitement.query.filter_by(requete_id=id).order_by(Traitement.id.desc()).all()[1:]
      return render_template("teacher/detail-requete.jinja",url=url,student=student,traitements=traitements,requetes=requetes, requete=requetep, justificatifs=justificatifs)
# @ui.roles_accepted('student')