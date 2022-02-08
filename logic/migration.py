import logging
from pdpyras import APISession
from logic.Key_data import KeyData


class Migration:
    _api_source_session = ""
    _api_destiny_session = ""

    def __init__(self, source_token, destiny_token):

        self._api_source_session = APISession(source_token)
        self._api_destiny_session = APISession(destiny_token)

    def start_migration(self):

        logging.info("Calling to get Teams data in source has been initiated ")

        origin_teams = self._get_teams(self._api_source_session)

        logging.info("Calling to delete Teams data in destination has been initiated ")

        self._delete_teams(self._api_destiny_session)

        logging.info("Calling to create Teams data in destination, from source data, has been initiated ")
        self._post_teams(origin_teams, self._api_destiny_session)

        return self._get_teams(self._api_destiny_session)

    def _get_teams(self, session):

        url = KeyData.GET_TEAM_API_URL.format(1000, 0, "false")
        response = session.get(url)

        if not response.ok:
            logging.error("Response Error - {0} - No data has been retriieved from API call at {1}".format(
                response.status_code, url))
            return None

        logging.info("Response OK - Success call Api: {0}".format(url))
        return response.json()['teams']

    def _delete_teams(self, session):

        for team in session.iter_all('teams'):
            logging.info("Deleting data at destination - URL: {0}".format(KeyData.DEL_TEAM_API_URL.format(team['id'])))
            response = session.delete(KeyData.DEL_TEAM_API_URL.format(team['id']))
            if not response.ok:
                logging.error("Error code {1} deleting data at destination with ID {0}".format(team['id'],
                                                                                               response.status_code))

        logging.info("Deleting data at destination has ended")

    def _post_teams(self, origin_teams, session):

        for team in origin_teams:
            team['name'] = team['name'] + "- {0} - Invalid Team".format(team['id'])
            logging.info("Data is being loaded at destination: {0}".format(format(team['name'])))
            result = session.post('/teams', json=team)
            if not result.ok:
                logging.error("Error code {1}: Data has not been loaded at destination: {0}".format(team['name'],
                                                                                                    result.status_code))
