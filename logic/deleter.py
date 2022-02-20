import atexit
import concurrent
import concurrent.futures
import os
from collections import namedtuple
from typing import List

from pdpyras import APISession

from logging_module.logger import logger
from logic.Key_data import KeyData


class Deleter:
    _api_destiny_session = ""

    def __init__(self, destiny_token):
        self._api_destiny_session = APISession(destiny_token)

    def start_deleting(self):
        list_teams = self.list_teams_to_delete(self._api_destiny_session)
        return self._delete(list_teams)

    def start_deleting_mp(self):
        list_teams = self.list_teams_to_delete(self._api_destiny_session)
        return self.__delete(list_teams)

    def start_deleting_mp_2(self, teams):
        # list_teams = self.list_teams_to_delete(self._api_destiny_session)
        list_teams: List[str] = []
        for team in teams:
            list_teams.append(team.id_param)
        return self.__delete(list_teams)

    def list_teams_to_delete(self, session):

        url = KeyData.GET_TEAM_API_URL.format(1000, 0, "false")
        response = session.get(url)

        if not response.ok:
            logger.error("Response - {0} - No data has been retrieved from API call at {1}".format(
                response.status_code, url))
            return None

        logger.info(" OK - Success call Api: {0}".format(url))
        teams = response.json()['teams']

        team_id: List[str] = []

        for team_x in teams:
            x = namedtuple("team", team_x.keys())(*team_x.values())
            team_id.append(x.id)

        return team_id

    # @staticmethod
    def _delete_teams(self, id_team):

        # session = self._api_destiny_session
        session = APISession(os.getenv("TOKEN_DESTINATION_WR"))
        response = session.delete(KeyData.DEL_TEAM_API_URL.format(id_team))
        if not response.ok:
            logger.error(
                "Error code {1} deleting data at destination with ID {0}".format(id_team, response.status_code))
            return False

        logger.info("Deleting data at destination has ended - {0} has been deleted".format(id_team))
        return True

    def _delete(self, list_teams):
        logger.info("Starting Deleting data as SYNC method at destination has ended")
        y = True
        for x in list_teams:
            if self._delete_teams(x) is False:
                y = False
        return y

    def __delete(self, list_teams):
        logger.info("Starting Deleting data as MultiProcessing method at destination has started")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self._delete_teams, list_teams)
        return True
