import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from logic.test import Test

# Press the green button in the gutter to run the script.

app = Flask(__name__)
CORS(app)


@app.route('/test/')
def test():
    return jsonify({"status": 200, "message": "test ok"})


# test_ = Test()
# return jsonify(test_.get_teams())


if __name__ == '__main__':
    app.run()
    # test = Test()
    # print(test.get_teams())
