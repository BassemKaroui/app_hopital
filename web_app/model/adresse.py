class Adresse:

    def __init__(self, id, num, rue, ville, region, code_postal, id_dossier_patient):
        self._id = id
        self._num = num
        self._rue = rue
        self._ville = ville
        self._region = region
        self._code_postal = code_postal
        self._id_dossier_patient = id_dossier_patient

    @property
    def id(self):
        return self._id

    @property
    def num(self):
        return self._num

    @property
    def rue(self):
        return self._rue

    @property
    def ville(self):
        return self._ville

    @property
    def region(self):
        return self._region

    @property
    def code_postal(self):
        return self._code_postal

    @property
    def id_dossier_patient(self):
        return self._id_dossier_patient

    @property
    def __dict__(self):
        return {
            "id": self._id,
            "num": self._num,
            "rue": self._rue,
            "ville": self._ville,
            "region": self._region,
            "code_postal": self._code_postal,
            "id_dossier_patient": self._id_dossier_patient
        }
