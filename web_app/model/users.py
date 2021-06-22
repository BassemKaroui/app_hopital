import jwt
import datetime


class Utilisateur():

    def __init__(self, id, nom, prenom, role, email):
        self._id = id
        self._prenom = prenom
        self._nom = nom
        self._role = role
        self._email = email
        self._token = ""

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def role(self):
        return self._role

    @property
    def email(self):
        return self._email

    def generation_token(self):
        payload = {
            # Date d'expiration : ici 3 minutes
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60),
            'iat': datetime.datetime.utcnow(),  # Date de la génération du token
            # Sujet (subjet) faisant l'objet du token : Ici l'id de l'utilisateur
            'idUser': self._id
        }
        self._token = jwt.encode(payload, "hopital_app", algorithm='HS256')

    @property
    def token(self):
        return self._token

    @property
    def __dict__(self):
        return {"id": self._id, "nom": self._nom, "prenom": self._prenom, "role": self._role, "email": self._email}
