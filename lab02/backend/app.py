from flask import Flask, request, jsonify
from flask_cors import CORS
from application.service import Service

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

service = Service()

@app.route('/list/<number>/<career>', methods=['GET'])
def get_list(number, career):
    response = service.get_list(number, career)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')