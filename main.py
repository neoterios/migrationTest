import logging
import os
import sys
import uuid

from dotenv import load_dotenv

from flask import Flask
import json
from flask_cors import CORS

from logic.migration import Migration

file_handler = logging.FileHandler(filename='logs/Migration.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    handlers=handlers)

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route('/start_migration/')
def get_migration():
    logging.info("Info - start_migration service has benn invoked")
    migration = Migration(os.getenv("TOKEN_PROVIDER"), os.getenv("TOKEN_DESTINATION_WR"))
    return json.dumps(migration.start_migration());


if __name__ == '__main__':
    app.run()
