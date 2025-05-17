from core.config import db
from .models import *
from core.auth.models import User, Role

statut_data = [
    dict(id=1, nom="suspendu"),
    dict(id=2, nom="termine"),
    dict(id=3, nom="rejeter"),
    dict(id=4, nom="validation"),
    dict(id=5, nom="en atente")]

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
    dict(id=1, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Modelisation", status="en attente"),
    dict(id=2, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Anglais", status="suspendu"),
    dict(id=3, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Informatique", status="rejeter"),
    dict(id=4, objet="absence de note", responsable_id="34ENTI023", etudiant_id="student1", intitule_ec="Geographie", status="terminer")

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