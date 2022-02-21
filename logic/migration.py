from pdpyras import APISession


class Migration:
    class MigrationSy:
        _api_source_session = ""
        _api_destiny_session = ""

        _source_token = ""
        _destiny_token = ""

        def __init__(self, source_token, destiny_token):
            self._source_token = source_token
            self._destiny_token = destiny_token

            self._api_source_session = APISession(source_token)
            self._api_destiny_session = APISession(destiny_token)