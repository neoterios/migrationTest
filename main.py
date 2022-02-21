import os
import uuid
from http import HTTPStatus

from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS

from logging_module.context import correlation_id
from logging_module.logger import logger
from logic.Key_data import KeyData
from logic.deleter import Deleter

from logic.migration_mp import MigrationMp
from logic.migration_sy import MigrationSy

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route('/start_migration_sy/')
def get_migration_sy():
    correlation_id.set(uuid.uuid4())
    logger.info("Info - start_migration_sy service has benn invoked")
    migration = MigrationSy(os.getenv("TOKEN_PROVIDER"), os.getenv("TOKEN_DESTINATION_WR"))
    resp = migration.start_migration()

    if resp.default_status != 200:
        logger.error("An Error has been detected saving origin data at destination, code  error {0}"
                     .format(resp.status_code))
        return Response("Error saving origin data at destination", resp.status_code, mimetype=KeyData.DATA_MIME_TYPE)

    logger.info("Data  migration has been  ended, status  code  {0}".format(resp.status_code))
    return resp

@app.route('/start_migration_mp/')
def get_migration_mp():
    correlation_id.set(uuid.uuid4())
    logger.info("Info - start_migration service has benn invoked")
    migration = MigrationMp(os.getenv("TOKEN_PROVIDER"), os.getenv("TOKEN_DESTINATION_WR"))
    resp = migration.start_migration_mp()

    if resp.default_status != 200:
        logger.error("An Error has been detected saving origin data at destination, code  error {0}"
                     .format(resp.status_code))
        return Response("Error saving origin data at destination", resp.status_code, mimetype=KeyData.DATA_MIME_TYPE)

    logger.info("Data  migration has been  ended, status  code  {0}".format(resp.status_code))
    return resp


@app.route('/delete/')
async def get_delete_sy():
    correlation_id.set(uuid.uuid4())
    logger.info("Info - Deleteting SYNC service has benn invoked")
    deleter = Deleter(os.getenv("TOKEN_DESTINATION_WR"))
    if deleter.start_deleting_sy() is False:
        return Response({"messagge": "Verifique los registros hubo una falla"}, HTTPStatus.BAD_REQUEST,
                        mimetype=KeyData.DATA_MIME_TYPE)

    return Response("Eliminacion exitosa", HTTPStatus.OK,
                    mimetype=KeyData.DATA_MIME_TYPE)


@app.route('/delete_mp/')
async def get_delete_mp():
    correlation_id.set(uuid.uuid4())
    logger.info("Info - Deleteting MULTY PROCESSING service has benn invoked")
    deleter = Deleter(os.getenv("TOKEN_DESTINATION_WR"))
    if deleter.start_deleting_mp() is False:
        return Response({"messagge": "Verifique los registros hubo una falla"}, HTTPStatus.BAD_REQUEST,
                        mimetype=KeyData.DATA_MIME_TYPE)

    return Response("Eliminacion exitosa", HTTPStatus.OK,
                    mimetype=KeyData.DATA_MIME_TYPE)


if __name__ == '__main__':
    app.run()
