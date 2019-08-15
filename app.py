from flask import Flask, request, redirect, url_for, send_from_directory, abort
from flask_cors import CORS, cross_origin

from work_materials.globals import PORT, mobs_queue

import json

app = Flask(__name__)
CORS(app)

#


@app.route('/addMob', methods=['POST', 'GET'])
def add_mob():
    print("Got request")
    js = request.get_json()
    if js is None:
        abort(400)
    print(js)
    mobs_queue.put(js)
    return json.dumps({"code": 200, "OK": True}, ensure_ascii=False)


def run_app():
    app.run(host='0.0.0.0', port=PORT)
    mobs_queue.put(None)
