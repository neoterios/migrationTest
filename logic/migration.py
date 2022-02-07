import os

from pdpyras import APISession

ORIGIN_TOKEN = os.getenv("TOKEN_PROVIDER")


def get_teams(token):

    session = APISession(token)

    response = session.get('/teams?limit=1000&offset=0&total=false')
    teams = None

    if response.ok:
        teams = response.json()['teams']

    return teams


class Migration:

    @classmethod
    def start_migration(self):
        # First Steep: get origin data
        origin_teams = get_teams(os.getenv("TOKEN_PROVIDER"))

        self.delete_teams(os.getenv("TOKEN_DESTINATION_WR"))

        self.post_teams(origin_teams, os.getenv("TOKEN_DESTINATION_WR"))

        return get_teams(os.getenv("TOKEN_DESTINATION_R"))

    # @staticmethod
    def delete_teams(token):

        session = APISession(token)

        for team in session.iter_all('teams'):
            response = session.delete("/teams/{0}".format(team['id']))

    def post_teams(origin_teams, token):
        session = APISession(token)

        for team in origin_teams:
            team['name'] = team['name'] + "- {0} - Invalid Team".format(team['id'])
            session.post('/teams', json=team)
