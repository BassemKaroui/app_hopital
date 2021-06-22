class ActeMedical:

    def __init__(self, id, code, description, tarification):
        self._id = id
        self._code = code
        self._description = description
        self._tarification = tarification

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    @property
    def description(self):
        return self._description

    @property
    def tarification(self):
        return self._tarification

    @property
    def __dict__(self):
        return {
            "id": self._id,
            "code": self._code,
            "description": self._description,
            "tarification": self._tarification
        }
