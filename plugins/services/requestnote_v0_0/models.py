from core.config import db
from datetime import datetime

class Etudiant(db.Model):
    __bind_key__ = 'requestnote_v0'
    __tablename__ = 'etudiants'
    id = db.Column(db.String(100), primary_key=True)
    nom = db.Column(db.String(100))
    classe = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    telephone = db.Column(db.String(100))
    requetes = db.relationship('Requete', backref='etudiants', lazy='dynamic')   

class Requete(db.Model):
    # blindage vers une bd
    __bind_key__ = 'requestnote_v0'
    __tablename__ = 'requetes'
    id = db.Column(db.Integer, primary_key=True)
    objet = db.Column(db.String(100))
    intitule_ec = db.Column(db.String(100))
    status = db.Column(db.String(100), default='en atente')
    piece = db.Column(db.String(100), nullable=True)
    responsable_id = db.Column(db.String(100), db.ForeignKey('responsables.id'), nullable=False)
    description = db.Column((db.Text), nullable=True)
    date_engr = db.Column((db.DateTime), default=datetime.utcnow)
    date_fin = db.Column((db.DateTime), nullable=True)
    etudiant_id = db.Column(db.String(100), db.ForeignKey('etudiants.id'), nullable=False)

    # responsable = db.relationship('Responsable', backref='requetes_gerees') 
    
    justificatifs = db.relationship('Justificatif', backref='requetes', lazy='dynamic')
    traitements = db.relationship('Traitement', backref='requetes', lazy='dynamic')

class Justificatif(db.Model):
    __bind_key__ = 'requestnote_v0'
    __tablename__ = 'justificatifs'
    id = db.Column(db.Integer, primary_key=True)
    justificatif = db.Column(db.String(255))
    libelle = db.Column(db.String(255))
    date_engr = db.Column((db.DateTime), default=datetime.utcnow)
    requete_id = db.Column(db.Integer, db.ForeignKey('requetes.id'), nullable=False)

class Responsable(db.Model):
    '''role'''
    __bind_key__ = 'requestnote_v0'
    __tablename__ = 'responsables'
    id = db.Column(db.String(100), primary_key=True)
    nom = db.Column(db.String(100))
    telephone = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    traitements = db.relationship('Traitement', backref='responsables', lazy='dynamic')

class Traitement(db.Model):
    __bind_key__ = 'requestnote_v0'
    __tablename__ = 'traitements'
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(255), nullable=True)
    date_tr = db.Column((db.Date), default=datetime.utcnow)
    requete_id = db.Column(db.Integer, db.ForeignKey('requetes.id'), nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('responsables.id'), nullable=False)
    statut_id = db.Column(db.Integer, db.ForeignKey('statuts.id'), nullable=False)

class Statut(db.Model):
    __bind_key__ = 'requestnote_v0'
    __tablename__ = 'statuts'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    traitements = db.relationship('Traitement', backref='statuts', lazy='dynamic')

