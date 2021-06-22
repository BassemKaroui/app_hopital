import datetime


class Consultation:

    def __init__(self, id, type, status, date_arrivee, anamnese, gravite, id_motif, id_transport, id_dossier_patient):
        self._id = id
        self._type = type
        self._status = status
        self._date_arrivee = date_arrivee
        self._anamnese = anamnese
        self._gravite = gravite
        self._id_motif = id_motif
        self._id_transport = id_transport
        self._id_dossier_patient = id_dossier_patient
        self._acte_medicaux = []
        self._soignants = []

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def status(self):
        return self._status

    @property
    def date_arrivee(self):
        return self._date_arrivee

    @property
    def anamnese(self):
        return self._anamnese

    @property
    def gravite(self):
        return self._gravite

    @property
    def id_motif(self):
        return self._id_motif

    @property
    def id_transport(self):
        return self._id_transport

    @property
    def id_dossier_patient(self):
        return self._id_dossier_patient

    def ajouter_acte_medical(self, acte_medical):
        self._acte_medicaux.append(acte_medical)

    def ajouter_soignant(self, utilisateur):
        self._soignants.append(utilisateur)

    @property
    def __dict__(self):
        return {
            "id": self._id,
            "type": self._type,
            "status": self._status,
            "date_arrivee": str(self._date_arrivee),
            "anamnese": self._anamnese,
            "gravite": self._gravite,
            "id_motif": self._id_motif,
            "id_transport": self._id_transport,
            "id_dossier_patient": self._id_dossier_patient,
            "acte_medicaux": [vars(acte_medical) for acte_medical in self._acte_medicaux],
            "soignants": [vars(utilisateur) for utilisateur in self._soignants]
        }
