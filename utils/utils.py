import json


class Util:

    @staticmethod
    def serialize(msg):
        return json.loads(
            json.dumps(msg, default=lambda o: getattr(o, '__dict__', str(o)))
        )
