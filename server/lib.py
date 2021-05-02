class AgentConflict(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def toDict(self):
        return {"message": self.message}
