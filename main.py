import logging
# import os
from dotenv import load_dotenv

from flask import Flask
import json
from flask_cors import CORS

from logic.migration import Migration

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route('/start_migration/')
def get_migration():
    migration = Migration()
    return json.dumps(migration.start_migration());


if __name__ == '__main__':
    app.run()
