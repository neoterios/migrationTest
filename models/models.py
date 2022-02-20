class Parents:
    def __init__(self, id_param: str = None, type_param: str = None, summary: str = None, self_param: str = None,
                 html_url: str = None):
        self.id_param = id_param
        self.type_param = type_param
        self.summary = summary
        self.self_param = self_param
        self.html_url = html_url


class Teams:
    def __init__(self, id_param: str = None, name: str = None, description: str = None, type_param: str = None,
                 summary: str = None, self_param: str = None, html_url: str = None,
                 default_role: str = None, parent: str = None):
        self.id_param = id_param
        self.name = name
        self.description = description
        self.type_param = type_param
        self.summary = summary
        self.self_param = self_param
        self.html_url = html_url
        self.default_role = default_role
        self.parent = parent


class SessionCallBack:
    teams: [Teams]
    def __init__(self, session_name: str, api_key: str):
        self.session_name = session_name
        self.api_key = api_key
        self.teams = []
