from flask import Flask, jsonify
from flask_cors import CORS
import requests
from application.backend.service import Service

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/list/<number>/<career>', methods=['GET'])
def getList(number, career):
    print("BACKEND: SOLICITUD RECIBIDA")
    res = Service().get_list(number, career)
    return jsonify(res), 200

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')