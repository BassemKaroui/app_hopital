import datetime


class DossierPatient:

    def __init__(self, id, ssn, nom, prenom, date_naissance, age, sexe):
        self._id = id
        self._ssn = ssn
        self._nom = nom
        self._prenom = prenom
        self._date_naissance = date_naissance
        self._age = age
        self._sexe = sexe
        self._consultations = []

    @property
    def id(self):
        return self._id

    @property
    def ssn(self):
        return self._ssn

    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def date_naissance(self):
        return self._date_naissance

    @property
    def age(self):
        return self._age

    @property
    def sexe(self):
        return self._sexe

    def ajouter_consultation(self, consultation):
        self._consultations.append(consultation)

    @property
    def __dict__(self):
        return {
            "id": self._id,
            "ssn": self._ssn,
            "nom": self._nom,
            "prenom": self._prenom,
            "date_naissance": str(self._date_naissance),
            "age": self._age,
            "sexe": self._sexe,
            "consultations": [vars(consultation) for consultation in self._consultations]}
