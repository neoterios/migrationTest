import concurrent
import concurrent.futures
import os

from logging_module.logger import logger
from collections import namedtuple
from http import HTTPStatus
from flask import Response
from pdpyras import APISession
from logic.Key_data import KeyData
from logic.deleter import Deleter
from models.models import Teams, SessionCallBack
from typing import List


class Migration:
    _api_source_session = ""
    _api_destiny_session = ""

    _source_token = ""
    _destiny_token = ""

    def __init__(self, source_token, destiny_token):

        self._source_token = source_token
        self._destiny_token = destiny_token

        self._api_source_session = APISession(source_token)
        self._api_destiny_session = APISession(destiny_token)

    def start_migration(self):

        logger.info("Calling to get Teams data in source has been initiated ")

        origin_teams = self._get_teams_o(self._api_source_session)

        if origin_teams is None:
            return Response("Error reading origin data", HTTPStatus.EXPECTATION_FAILED, mimetype=KeyData.DATA_MIME_TYPE)

        logger.info("Calling to delete Teams data in destination has been initiated ")

        if self._delete_teams(self._api_destiny_session) is False:
            return Response("Error erasing data at destination", HTTPStatus.EXPECTATION_FAILED,
                            mimetype=KeyData.DATA_MIME_TYPE)

        logger.info("Calling to create Teams data in destination, from source data, has been initiated ")
        if self._post_teams(origin_teams, self._api_destiny_session) is False:
            return Response("Error saving data at destination", HTTPStatus.EXPECTATION_FAILED,
                            mimetype=KeyData.DATA_MIME_TYPE)

        result = self.list_teams(self._api_destiny_session)
        if result is None:
            return Response("Error saving data at destination", HTTPStatus.EXPECTATION_FAILED,
                            mimetype=KeyData.DATA_MIME_TYPE)
        logger.info("Record data in destination, from source data, has been successfully")

        return Response(result, HTTPStatus.OK, mimetype=KeyData.DATA_MIME_TYPE)

    def start_migration_mp(self):

        logger.info("Calling to get Teams data in source has been initiated ")

        list_sessions_tkn: [str] = []
        list_sessions_tkn.append(SessionCallBack("origin", self._source_token))
        list_sessions_tkn.append(SessionCallBack("destiny", self._destiny_token))
        result: [SessionCallBack] = self.load_teams(list_sessions_tkn)

        origin_teams = None
        destiny_teams = None

        for item in result:
            if (item.session_name == "origin"):
                origin_teams = item.teams
            if (item.session_name == "destiny"):
                destiny_teams = item.teams

        if origin_teams is None:
            return Response("Error reading origin data", HTTPStatus.EXPECTATION_FAILED, mimetype=KeyData.DATA_MIME_TYPE)

        logger.info("Calling to delete Teams data in destination has been initiated ")

        deleter = Deleter(os.getenv("TOKEN_DESTINATION_WR"))
        if deleter.start_deleting_mp_2(destiny_teams) is False:
            return Response("Error erasing data at destination", HTTPStatus.EXPECTATION_FAILED,
                            mimetype=KeyData.DATA_MIME_TYPE)

        logger.info("Calling to create Teams data in destination, from source data, has been initiated ")
        #if self._post_teams(origin_teams, self._api_destiny_session) is False:
        if self._post_teams_mp(origin_teams, self._destiny_token) is False:
            return Response("Error saving data at destination", HTTPStatus.EXPECTATION_FAILED,
                            mimetype=KeyData.DATA_MIME_TYPE)

        result = self.list_teams(self._api_destiny_session)
        if result is None:
            return Response("Error saving data at destination", HTTPStatus.EXPECTATION_FAILED,
                            mimetype=KeyData.DATA_MIME_TYPE)
        logger.info("Record data in destination, from source data, has been successfully")

        return Response(result, HTTPStatus.OK, mimetype=KeyData.DATA_MIME_TYPE)

    @staticmethod
    def _get_teams(session_call_back: SessionCallBack):

        session = APISession(session_call_back.api_key)

        logger.info("Starting retrieve team - {0}".format(session_call_back.session_name))

        url = KeyData.GET_TEAM_API_URL.format(1000, 0, "false")
        response = session.get(url)

        if not response.ok:
            logger.error("Response - {0} - No data has been retrieved from API call at {1}".format(
                response.status_code, url))
            return None

        logger.info(" OK - Retrieved team successfully - {1} - Success call Api: {0}"
                    .format(url, session_call_back.session_name))

        teams = response.json()['teams']

        team_: List[Teams] = []

        for team_x in teams:
            x = namedtuple("team", team_x.keys())(*team_x.values())

            team_.append(Teams(id_param=x.id, name=x.name, description=x.description, type_param=x.type,
                               summary=x.summary, self_param=x.self, html_url=x.html_url,
                               default_role=x.default_role, parent=x.parent))
        session_call_back.teams = team_

        return session_call_back

    @staticmethod
    def _get_teams_o(session):

        logger.info("Starting retrieve team -")

        url = KeyData.GET_TEAM_API_URL.format(1000, 0, "false")
        response = session.get(url)

        if not response.ok:
            logger.error("Response - {0} - No data has been retrieved from API call at {1}".format(
                response.status_code, url))
            return None

        logger.info(" OK - Retrieved team successfully - Success call Api: {0}".format(url))
        teams = response.json()['teams']

        team_: List[Teams] = []

        for team_x in teams:
            x = namedtuple("team", team_x.keys())(*team_x.values())

            team_.append(Teams(id_param=x.id, name=x.name, description=x.description, type_param=x.type,
                               summary=x.summary, self_param=x.self, html_url=x.html_url,
                               default_role=x.default_role, parent=x.parent))
        return team_

    @staticmethod
    def get_teams(session):

        url = KeyData.GET_TEAM_API_URL.format(1000, 0, "false")
        response = session.get(url)

        if not response.ok:
            logger.error("Response Error - {0} - No data has been retrieved from API call at {1}".format(
                response.status_code, url))
            return None

        logger.info("Response OK - Success call Api: {0}".format(url))
        teams = response.json()['teams']

        team_: List[Teams] = []

        for team_x in teams:
            x = namedtuple("team", team_x.keys())(*team_x.values())

            team_.append(Teams(id_param=x.id, name=x.name, description=x.description, type_param=x.type,
                               summary=x.summary, self_param=x.self, html_url=x.html_url,
                               default_role=x.default_role, parent=x.parent))
        return team_

    @staticmethod
    def list_teams(session):
        url = KeyData.GET_TEAM_API_URL.format(1000, 0, "true")
        response = session.get(url)

        if not response.ok:
            logger.error("Response Error - {0} - No data has been retrieved from API call at {1}".format(
                response.status_code, url))
            return None

        return response.text

    @staticmethod
    def _delete_teams(session):

        for team in session.iter_all('teams'):
            logger.info("Deleting data at destination - URL: {0}".format(KeyData.DEL_TEAM_API_URL.format(team['id'])))
            response = session.delete(KeyData.DEL_TEAM_API_URL.format(team['id']))
            if not response.ok:
                logger.error("Error code {1} deleting data at destination with ID {0}".format(team['id'],
                                                                                              response.status_code))
                return False

        logger.info("Deleting data at destination has ended")
        return True


    def _post_teams_mp(self, origin_teams, api_token):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            x = executor.map(self._post_teams_mp_ex, origin_teams)
            return True

    def _post_teams_mp_ex(self, team: Teams):
        logger.info("Data is being loaded at destination: {0}".format(format(team.name)))

        session = APISession(self._destiny_token)
        team.name = team.name + "- {0} - Invalid Team".format(team.id_param)
        result = session.post('/teams', json=team.__dict__)

        if result.ok is False:
            logger.error("Error code {1}: Data has not been loaded at destination: {0}"
                         .format(team['name'], result.status_code))
            return False

        return True

    @staticmethod
    def _post_teams(origin_teams: [Teams], session):

        try:
            for team in origin_teams:
                team.name = team.name + "- {0} - Invalid Team".format(team.id_param)
                logger.info("Data is being loaded at destination: {0}".format(format(team.name)))
                result = session.post('/teams', json=team.__dict__)
                if result.ok is False:
                    logger.error("Error code {1}: Data has not been loaded at destination: {0}"
                                 .format(team['name'], result.status_code))
                    return False
            return True

        except NotImplementedError:
            return False
        except AttributeError:
            logger.error("System Error: a error has been raised, please contact your admin")
            return False

    @staticmethod
    def _post_teams_(origin_teams, session):

        for team in origin_teams:
            team['name'] = team['name'] + "- {0} - Invalid Team".format(team['id'])
            logger.info("Data is being loaded at destination: {0}".format(format(team['name'])))
            result = session.post('/teams', json=team)
            if not result.ok:
                logger.error("Error code {1}: Data has not been loaded at destination: {0}"
                             .format(team['name'], result.status_code))

    def load_teams(self, list_sessions: [SessionCallBack]):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.map(self._get_teams, list_sessions)
            response_list: [SessionCallBack] = []
            for item in future:
                response_list.append(item)
            return response_list
