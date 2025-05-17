from core.config import db
from .models import *
from core.auth.models import User, Role
from datetime import datetime

student_data = [
    dict(id="22NTI010A", nom="KENFACK ROMEO", classe="II2", email="nanaromeo237@gmail.com", telephone="655927237"),
    dict(id="22NTI011A", nom="MAKOUHO ORNELLE ALICE", classe="TIC3", email="prodistributionltb1@gmail.com", telephone="655521434"),
    dict(id="22NTI012I", nom="TENEKE CARLOS ARNAUD", classe="GCI3", email="nanaromeo233@gmail.com", telephone="657501933"),
]

responsable_data = [
    dict(id="34ENTI023", nom="MALCOM PENDA", email="nanaromeo237@gmail.com", telephone="679243290"),
    dict(id="34ENTI025", nom="TACHIUEM YVES BRYAN", email="prodistributionltd3@gmail.com", telephone="679243290"),
    dict(id="34ENTI029", nom="La mauvaise compagnie", email="65750193t@gmail.com", telephone="679243220"),
    dict(id="34ENTI030", nom="NNEME JORDAN", email="prodistributionltd5@gmail.com", telephone="679243220"),
]

role_data = [
    dict(id="chef_depart", name="chef_departement"),
    dict(id="cellule", name="cellule"),
    dict(id="directeur", name="directeur"),
]

user_data = [
    dict(id="22NTI010A", pwd="password1", role="student"),
    dict(id="22NTI011A", pwd="password1", role="student"),
    dict(id="22NTI012I", pwd="password1", role="student"),

    dict(id="34ENTI023", pwd="password1", role="teacher"),
    dict(id="34ENTI025", pwd="password1", role="chef_depart"),
    dict(id="34ENTI029", pwd="password1", role="cellule"),
    dict(id="34ENTI030", pwd="password1", role="directeur"),
]

requete_data = [
    dict(id=1, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Modelisation", status="terminer"),
    dict(id=2, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Anglais", status="suspendu"),
    dict(id=3, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Informatique", status="rejeter"),
    dict(id=4, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Geographie", status="approuver", date_fin=datetime.utcnow()),
    dict(id=5, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Geographie", status="approuver"),
    dict(id=6, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Modelisation", status="en attente"),

] 

statut_data = [
    dict(id=1, nom="suspendu", color="dark"),
    dict(id=2, nom="termine", color="success"),
    dict(id=3, nom="rejeter", color="danger"),
    dict(id=4, nom="approuver", color="warning"),
    dict(id=5, nom="en attente", color="secondary")]

traitement_data =[
    dict(id=1, commentaire="Les requetes ne sont plus recevable", requete_id=5, responsable_id="34ENTI023", statut_id=4, date_tr=datetime.utcnow()),
    dict(id=2, commentaire="Les requetes ne sont plus recevable", requete_id=3, responsable_id="34ENTI023",statut_id=3, date_tr=datetime.utcnow()),
    dict(id=3, commentaire="envoyer vos recus de paiement", requete_id=2, responsable_id="34ENTI023", statut_id=1, date_tr=datetime.utcnow()),
    dict(id=4, commentaire="Les requetes ne sont plus recevable", requete_id=4, responsable_id="34ENTI023", statut_id=4, date_tr=datetime.utcnow()),
    dict(id=5, commentaire="Votre note a ete modifier 13 au lieu de 10", requete_id=1, responsable_id="34ENTI023",statut_id=5, date_tr=datetime.utcnow()),
    dict(id=6, commentaire="envoyer vos recus de paiement", requete_id=1, responsable_id="34ENTI023",statut_id=1, date_tr=datetime.utcnow()),
    dict(id=7, commentaire="", requete_id=1, responsable_id="34ENTI023",statut_id=4, date_tr=datetime.utcnow()),
    dict(id=8, commentaire="Votre note a ete modifier 13 au lieu de 10", requete_id=1, responsable_id="34ENTI023",statut_id=2, date_tr=datetime.utcnow()),
    dict(id=9, commentaire="Votre note a ete modifier 13 au lieu de 10", requete_id=6, responsable_id="34ENTI023",statut_id=5, date_tr=datetime.utcnow())

]
def init_data():

    for row in statut_data:
        statut = Statut(**row)
        db.session.merge(statut)
    db.session.commit()
    
    for row in student_data:
        student = Etudiant(**row)
        db.session.merge(student)
    db.session.commit()
    
    for row in responsable_data:
        responsable = Responsable(**row)
        db.session.merge(responsable)
    db.session.commit()
    
    for row in role_data:
        role = Role(**row)
        db.session.merge(role)
    db.session.commit()
    
    for row in user_data:
        user = User(id=row['id'], roles=[role])
        user.set_password(row['pwd'])
        db.session.merge(user)
    db.session.commit()

    for row in requete_data:
        requete = Requete(**row)
        # user.set_password(row['pwd'])
        db.session.merge(requete)
    db.session.commit()

    for row in traitement_data:
        traitement = Traitement(**row)
        # user.set_password(row['pwd'])
        db.session.merge(traitement)
    db.session.commit()