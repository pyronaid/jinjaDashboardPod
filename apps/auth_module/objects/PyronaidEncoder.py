from json import JSONEncoder


class PyronaidEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
