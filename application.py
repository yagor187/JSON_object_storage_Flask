from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from cache import write_file, open_file
import time

app = Flask(__name__)
metrics = PrometheusMetrics(app)
object_storage = open_file()


@app.route('/objects/<string:key>', methods=['PUT'])
def put_object(key):
    try:
        data = request.get_json()
        object_storage[key] = data
        expiry_time = request.headers.get('Expires')
        if expiry_time is not None:
            object_storage[key]["expires_time"] = int(expiry_time) + int(time.time())
        write_file(object_storage)
        return jsonify({'message': 'saved successful'}), 200
    except Exception as e:
        return jsonify({'error1': str(e)}), 500

@app.route('/objects/<key>', methods=['GET'])
def get_object(key):
    if key in object_storage:
        data = object_storage[key]
        return jsonify(data), 200
    else:
        return jsonify({'error2': 'Object not found'}), 404

@app.route('/', methods=['GET'])
def get_all_object():
    if object_storage:
        data = object_storage
        return jsonify(data), 200
    else:
        return jsonify("Storage is empty"), 200

@app.route("/probes/liveness", methods=["GET"])
def liveness_check():
    return jsonify(status="alive"), 200

@app.route("/probes/readiness", methods=["GET"])
def readiness_check():
    return jsonify(status="ready"), 200


