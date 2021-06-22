# set FLASK_APP=web_app
# set FLASK_ENV=development
# set FLASK_DEBUG=1
# flask run

# ---------------------------------
# LIBRAIRIES
# ---------------------------------

import datetime

# FLASK et OS
import sys
from web_app.model import dossierPatient

from flask import Flask
import os
from flask import render_template

# JSON
import json
from flask import jsonify

# COMMUNICATION
from flask import request

# ---------------------------------
# MODELES
# ---------------------------------

from .model import Utilisateur
from .model import DossierPatient
from .model import ActeMedical
from .model import MotifRecours
from .model import ModeTransport
from .model import Consultation

# --------------------------------
# SECURISATION
# --------------------------------
from functools import wraps
import jwt
from flask import session
from flask import current_app, g
from flask import redirect
from flask import url_for

# ---------------------------------
# BASES DE DONNEES
# ---------------------------------
import sqlalchemy
from sqlalchemy.orm import scoped_session
from .database import SessionSQLAlchemyGlobale, engine

# # On note l'utilisation de l'Alias pour éviter de porter le même nom que l'objet métier Piece
from .dao import Utilisateur as UtilisateurDAO
# # On note l'utilisation de l'Alias pour éviter de porter le même nom que l'objet métier Capteur
from .dao import Consultation as ConsultationDAO
from .dao import DossierPatient as DossierPatientDAO
from .dao import Adresse as AdresseDAO
from .dao import ActeMedical as ActeMedicalDAO
from .dao import MotifRecours as MotifRecoursDAO
from .dao import ModeTransport as ModeTransportDAO
from .dao import ConsultationUtilisateur as ConsultationUtilisateurDAO

# Creation de la base de donnée de façon automatique
dao.Base.metadata.create_all(bind=engine)

# Recuperation de la session
sessionBDD = SessionSQLAlchemyGlobale()


# Fonction de création de l'application

def create_app():

    # ---------------------------------------------------------------------
    # INITIALISATION DE L'APPLICATION
    # ----------------------------------------------------------------------

    # Instanciation du Framework Flask -> Application
    app = Flask(__name__)

    # On s'assure que le fichier d'instance est bien créé (Sinon pas de possibilité de créer la BDD)
    try:
        os.makedirs(app.instance_path)
        print("Repertoire cree")  # uniquement aprés rechargement de la page
    except OSError:
        pass

    # Securisation API : On créé un utilisateur et on récupere son Token
    # Ce token et généralement stocké en base de donnée pour chacun des utilisateurs
    # Le token doit être communiqué au client pour qu'il puisse l'utiliser dans son application

    # -------------------------------------------------
    # SECURISATION DE L'APPLICATION WEB
    # -------------------------------------------------

    # Securisation de l'application
    app.config.from_mapping(
        # Clé secrète pour la session
        # A noter que cette clé secrete peut aussi etre utilisée pour les apis.
        SECRET_KEY='hopital_app'
    )

    # Avant l'execution d'une requete, on vérifier la présence de l'utilisateur

    @app.before_request
    def avant_execution_requete():

        # On recupere l'id utilisateur
        user_id = session.get('user_id')
        print(user_id)

        # Si pas d'id, cela signifie que l'on est pas connecté
        if user_id is None:
            # g.utilisateur = None
            print("PAS DE USER !")
        else:
            # On recherche l'utilisateur en BDD et on stock l'objet en mémoire
            # Pourquoi ne pas l'avoir fait lors du login ?
            # Parce que g n'est accessible qu'avant l'execution d'une requete...
            print("USER CONNU")
            # g.utilisateur = Utilisateur(1, 'Bassem', 'Karoui')

    # Creation d'un décorateur spécifique

    def connexion_requise(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if session.get('user_id') is None:  # g.utilisateur
                return redirect(url_for('login'))

            return view(*args, **kwargs)

        return wrapped_view

    # ---------------------------------------------------------------------
    # VUES (PAGES HTML)
    # ----------------------------------------------------------------------

    # Creation d'une premiere route

    @app.route('/')
    @connexion_requise
    def accueil():
        if session['user_role'] == 0:
            return render_template('administration.html')
        else:
            return render_template('consultation.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @connexion_requise
    @app.route('/administration')
    def administration():
        if session['user_role'] != 0:
            return redirect(url_for('accueil'))
        return render_template('administration.html')

    @connexion_requise
    @app.route('/consultation')
    def consultation():
        if session['user_role'] not in (1, 2):
            return redirect(url_for('accueil'))
        return render_template('consultation.html')

    # ---------------------------------------------------------------------
    # APIs
    # ----------------------------------------------------------------------
    @app.route('/consultation/sauvegarde', methods=['POST'])
    def SaveFile():
        # Récupération des données
        datasDictionnary = request.json
        messageRecu = ""
        for data in datasDictionnary:
            role = data["role"]
            id_consultation = data["consultation"]
            ssn = data["ssn"]
            nom_patient = data["Nom"]
            prenom_patient = data["Prenom"]
            age = data["Age"]
            sexe = data["Sexe"]
            date_naissance = data["Date_naissance"]
            id_recours = data["recours"]
            id_gravite = data["gravite"]
            id_transport = data["transport"]
            anamnese = data["anamnese"]
            date_arrivee = data["Date_arrivee"]
            actes_medicaux = data["actes_medicaux"]

        print(data)

        if role == "1":
            print(role)
            oConsultationDao = sessionBDD.query(ConsultationDAO).filter(
                ConsultationDAO.id == id_consultation).one()
            print("DAO consult", oConsultationDao.id, oConsultationDao.anamnese)
            sessionBDD.query(ConsultationDAO).filter(ConsultationDAO.id == id_consultation).update(
                {"id_motif": id_recours, "id_transport": id_transport, "gravite": id_gravite, "anamnese": anamnese}, synchronize_session="fetch")
            sessionBDD.commit()

            print(f"Piece {oConsultationDao.id} modifiée")
        elif role == "2":
            print(role)
            oConsultationDao = sessionBDD.query(ConsultationDAO).filter(
                ConsultationDAO.id == id_consultation).one()
            print("DAO consult", oConsultationDao.id, oConsultationDao.anamnese)
            sessionBDD.query(ConsultationDAO).filter(ConsultationDAO.id == id_consultation).update(
                {"status": "fermé", "id_motif": id_recours, "id_transport": id_transport, "gravite": id_gravite, "anamnese": anamnese}, synchronize_session="fetch")
            sessionBDD.commit()

        # dico
        dictionnaireReponse = {"data": []}

        return jsonify(dictionnaireReponse)

    @app.route('/consultation/GetUserTime', methods=['GET'])
    def getUserTime():

        # dico
        dico_data = {}

        # Dictionnaire de réponse
        dictionnaireReponse = {"data": []}
        user_id = session.get('user_id')

        # On récupère le user
        SoignantDAO = sessionBDD.query(UtilisateurDAO).filter(
            UtilisateurDAO.id == user_id).one()

        oSoignant = Utilisateur(SoignantDAO.id, SoignantDAO.nom,
                                SoignantDAO.prenom, SoignantDAO.role, SoignantDAO.email)

        print(oSoignant.__dict__)

        # On récupère la date
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        dico_data["date"] = dt_string
        dico_data["user"] = oSoignant.__dict__
        dictionnaireReponse["data"].append(dico_data)
        return jsonify(dictionnaireReponse)

    @app.route('/consultation/listeMotif', methods=['GET'])
    def getMotifs():

        # Récupération des motifs en BDD
        motifs = sessionBDD.query(MotifRecoursDAO).all()

        # Récupération des transports en BDD
        transports = sessionBDD.query(ModeTransportDAO).all()

        # Dictionnaire de réponse
        dictionnaireReponse = {"data": [], "transport": []}

        # Récupération des motifs
        for motifdao in motifs:
            oMotif = MotifRecours(motifdao.id, motifdao.description)
            dictionnaireReponse["data"].append(oMotif.__dict__)

        # Récupération des tranports
        for transportdao in transports:
            oTransport = ModeTransport(
                transportdao.id, transportdao.description)
            dictionnaireReponse["transport"].append(oTransport.__dict__)

        return jsonify(dictionnaireReponse)

    @app.route('/consultation/searchmot', methods=['POST'])
    def postMot():

        # initialisation
        dico_reponse = {"data": []}

        # Message recu lorsque l'on appuie sur le bouton
        datasDictionnary = request.json
        messageRecu = ""
        filtre = ""

        for data in datasDictionnary:
            messageRecu = data["message"]
            filtre = data["filtre"]

        if filtre == "1":

            actes = sessionBDD.query(ActeMedicalDAO).filter(
                ActeMedicalDAO.description.like(messageRecu + "%"))

            for oacteDAO in actes:
                oActe = ActeMedical(oacteDAO.id, oacteDAO.code,
                                    oacteDAO.description, oacteDAO.tarification)
                dico_reponse["data"].append(oActe.__dict__)
                print(oacteDAO.description)
        else:
            actes = sessionBDD.query(ActeMedicalDAO).filter(
                ActeMedicalDAO.code.like(messageRecu + "%"))

            for oacteDAO in actes:
                oActe = ActeMedical(oacteDAO.id, oacteDAO.code,
                                    oacteDAO.description, oacteDAO.tarification)
                dico_reponse["data"].append(oActe.__dict__)
                print(oacteDAO.code)

        print(filtre)
        return jsonify(dico_reponse)

    # Recherche du numero pour la consultation
    @app.route('/consultation/modifyConsult', methods=['POST'])
    def modify_consult():

        # reception message
        datasDictionnary = request.json
        code_ssn = ""
        for data in datasDictionnary:
            code_ssn = data["code"]
        print(code_ssn)

        dico_reponse = {"data": [], "search_statut": False}

        # Récupération du dossier dao du patient
        try:
            # Dossier DAO
            oDossierDao = sessionBDD.query(DossierPatientDAO).filter(
                DossierPatientDAO.ssn == code_ssn).one()

            # Creation de l'objet
            oDossier = DossierPatient(oDossierDao.id, oDossierDao.ssn, oDossierDao.nom,
                                      oDossierDao.prenom, oDossierDao.date_naissance, oDossierDao.age, oDossierDao.sexe)

            for oConsultationDao in oDossierDao.consultation:
                oConsultation = Consultation(oConsultationDao.id, oConsultationDao.type, oConsultationDao.status, oConsultationDao.date_arrivee, oConsultationDao.anamnese,
                                             oConsultationDao.gravite, oConsultationDao.id_motif, oConsultationDao.id_transport, oConsultationDao.id_dossier_patient)

                # Pour chaque consultation on récupère les actes médicaux
                for oActeMedicalDao in oConsultationDao.acte_medicaux:

                    oActeMedical = ActeMedical(
                        oActeMedicalDao.id, oActeMedicalDao.code, oActeMedicalDao.description, oActeMedicalDao.tarification)

                    # On ajoute à la consultation les actes médicaux
                    oConsultation.ajouter_acte_medical(oActeMedical)

                # On ajoute au dossier la consultation
                oDossier.ajouter_consultation(oConsultation)

            print(vars(oDossier))
            dico_reponse["data"].append(oDossier.__dict__)

            search_status = True

        except:
            search_status = False

        # Retour du resultat de la recherche
        dico_reponse["search_statut"] = search_status
        print(dico_reponse)

        return jsonify(dico_reponse)

    # Recuperer toutes les consultations
    @app.route('/administration/getConsultations', methods=['GET'])
    def getConsultations():

        dico_reponse = {"data": []}

        print("debut requete BDD getConsultations")
        ConsultationsDAO = sessionBDD.query(ConsultationDAO).filter(
            ConsultationDAO.status == "ouvert").all()

        print("fin requete BDD getConsultations")

        for oConsultationDao in ConsultationsDAO:
            oConsultation = Consultation(oConsultationDao.id, oConsultationDao.type, oConsultationDao.status, oConsultationDao.date_arrivee, oConsultationDao.anamnese,
                                         oConsultationDao.gravite, oConsultationDao.id_motif, oConsultationDao.id_transport, oConsultationDao.id_dossier_patient)

            DossiersPatientsDAO = sessionBDD.query(DossierPatientDAO).filter(
                DossierPatientDAO.id == oConsultation.id_dossier_patient).one()
            oDossierPatient = DossierPatient(DossiersPatientsDAO.id, DossiersPatientsDAO.ssn, DossiersPatientsDAO.nom,
                                             DossiersPatientsDAO.prenom, DossiersPatientsDAO.date_naissance, DossiersPatientsDAO.age, DossiersPatientsDAO.sexe)
            response = {
                "id": oConsultation._id,
                "status": oConsultation._status,
                "date_arrivee": str(oConsultation._date_arrivee),
                "nom": oDossierPatient._nom,
                "prenom": oDossierPatient._prenom
            }

            dico_reponse["data"].append(response)

        return jsonify(dico_reponse)

    # Recherche du numero de securite sociale dans la base de donnees
    @app.route('/administration/searchByNumSS', methods=['POST'])
    def search():
        # reception message
        datasDictionnary = request.json
        messageRecu = ""
        for data in datasDictionnary:
            messageRecu = data["message"]
        print(messageRecu)

        # initialisation du resultat de la recherche
        dict = {"data": []}
        datas = {}

        # Récupération du dossier du patient
        try:
            oDossierDao = sessionBDD.query(DossierPatientDAO).filter(
                DossierPatientDAO.ssn == messageRecu).one()
            search_status = True
            datas["nom"] = oDossierDao.nom
            datas["prenom"] = oDossierDao.prenom
            datas["dateNaissance"] = str(oDossierDao.date_naissance)
            datas["age"] = oDossierDao.age
            datas["sexe"] = oDossierDao.sexe
            oAdresseDao = sessionBDD.query(AdresseDAO).filter(
                AdresseDAO.id_dossier_patient == oDossierDao.id).one()
            datas["numRue"] = oAdresseDao.num
            datas["rue"] = oAdresseDao.rue
            datas["ville"] = oAdresseDao.ville
            datas["region"] = oAdresseDao.region
            datas["codePostal"] = oAdresseDao.code_postal
        except:
            search_status = False

        datas["search_status"] = search_status
        dict["data"].append(datas)
        return jsonify(dict)

    @app.route('/administration/ajoutConsultation', methods=['POST'])
    def ajoutConsultation():
        datasDictionnary = request.json
        for data in datasDictionnary:
            ssn = data["ssn"]
            nom = data["nom"]
            prenom = data["prenom"]
            dateNaissance = datetime.date.fromisoformat(data["dateNaissance"])
            age = data["age"]
            sexe = data["sexe"]
            numRue = data["numRue"]
            rue = data["rue"]
            codePostal = data["codePostal"]
            ville = data["ville"]
            region = data["region"]
            motifRecours = data["motifRecours"]
            modeTransport = data["modeTransport"]

        try:
            oDossierPatientDao = sessionBDD.query(DossierPatientDAO).filter(
                DossierPatientDAO.ssn == ssn).one()
            search_status = True
        except:
            oDossierPatientDao = DossierPatientDAO(
                ssn=ssn, nom=nom, prenom=prenom, date_naissance=dateNaissance, age=age, sexe=sexe)
            oAdresseDao = AdresseDAO(num=numRue, rue=rue, ville=ville, region=region,
                                     code_postal=codePostal)
            oDossierPatientDao.adresse.append(oAdresseDao)
            sessionBDD.add(oAdresseDao)
            sessionBDD.add(oDossierPatientDao)
            search_status = False

        oConsultationDao = ConsultationDAO(
            id_motif=motifRecours, id_transport=modeTransport)
        oDossierPatientDao.consultation.append(oConsultationDao)
        sessionBDD.add(oConsultationDao)
        sessionBDD.commit()

        dict = {"data": []}
        return jsonify(dict)

    @app.route('/api/loginCheck', methods=["POST"])
    def loginCheck():
        # @Todo : A coder par vos soins
        # On récupere les logins et mot de passe depuis le formulaire
        # On cherche l'utilisateur en base de données

        # Simulation pour l'exemple... ;-)
        data = request.json
        email = data['email']
        password = data['password']

        try:
            user_dao = sessionBDD.query(UtilisateurDAO).filter(
                UtilisateurDAO.email == email).one()
        except sqlalchemy.exc.NoResultFound:
            return '{"message":"erreur"}'
        db_password = user_dao.password

        connecte = False
        if password == db_password:
            connecte = True
            user = Utilisateur(user_dao.id, user_dao.nom,
                               user_dao.prenom, user_dao.role, user_dao.email)
            user.generation_token()

        # Si on trouve l'utilisateur, on le stocke en session (Une cle secrete est necessaire)
        # La session est 'vivante' tant que le navigateur reste ouvert
        # Pour tester, utiliser le mode navigation privée
        # On renvoi une réponse positive à la vue
        if (connecte == True):
            session.clear()
            session['user_id'] = user.id
            session['token'] = user.token
            session['user_role'] = user.role
            print(session['user_role'])
            return '{"message":"ok"}'
        else:
            return '{"message":"erreur"}'

    @app.route('/api/logout')
    def logout():
        session.pop('user_id')
        session.pop('token')
        session.pop('user_role')
        return redirect(url_for('login'))

    ################################################
    # Planification
    ################################################

    # @app.route('/api/planification')
    # def planification():
    #     data = request.json
    #     date = datetime.datetime.fromisoformat(data["date"])
    #     sessionBDD.query(ConsultationUtilisateurDAO).filter(
    #         ConsultationUtilisateurDAO.email == email).one()
    #     return

    # Creation d'un décorateur spécifique
    def securisation_token(f):
        @ wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
                print("Token recu :", token)
            if not token:
                print("Parametre X-ACCESS Non recu")
                return 'Acces non autorisé !', 401

            # Decodage :
            try:
                # Attention algorithms prend un s !!
                data = jwt.decode(token, "hopital_app", algorithms='HS256')
                print("Décodage : ", data)
                id = data["idUser"]
                print("Id utilisateur : ", id)

                # Recherche de l'utilisateur dans la base de donnée :
                # Si trouvé = Acces ok
                # Si pas trouvé = Acces non authorisé
                utilisateur_trouve = False
                if int(id) == 1:
                    # On renvoi vrai, ce qui signifie que l'on donne access à l'API
                    utilisateur_trouve = True

                if not utilisateur_trouve:
                    return 'Access non authorisé !', 401

            except:
                print("Autre raison (delai dépassé...)")
                return 'Access non authorisé !', 404

            return f(*args, **kwargs)

        return decorated

    return app
