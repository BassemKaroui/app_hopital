class ModeTransport:

    def __init__(self, id, description):
        self._id = id
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def __dict__(self):
        return {
            "id": self._id,
            "description": self._description
        }
