from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from ..db.model import Alumno, CarreraProfesional

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

URL_REPOSITORY = "http://127.0.0.1:3001"

@app.route('/list/<number>/<career>', methods=['GET'])
def getList(number, career):
    print("BACKEND: SOLICITUD RECIBIDA")
    res = requests.get(URL_REPOSITORY+'/tables/talumno')
    data = res.json()
    print("DATA alumno RECIBIDA")
    
    alumnos = []
    for row in data["data"]:
        alumno = Alumno(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        alumnos.append(alumno)

    #print(f"Alumnos: {alumnos}")

    res = requests.get(URL_REPOSITORY+'/tables/tcarreraprofesional')
    data = res.json()
    print("DATA carrera RECIBIDA")
    #print(data)

    carreras = []
    for carrera in data['data']:
        carrera = CarreraProfesional(carrera[0], carrera[1], carrera[2], carrera[3], alumnos)
        carreras.append(carrera)
        
    if number == "1":
        rows = [carrera.getList1() for carrera in carreras]
        cols = ["Código", "Nombre", "Fecha Creación", "Observación", "Cantidad de alumnos"]
    elif number == "2":
        if career == "none":
            rows = [carrera.nombre for carrera in carreras]
            cols = []
        else:
            cols = ["Código", "Nombres", "Apellidos", "Edad", "Sexo", "Peso", "Talla", "Color", "Provincia", "Código Carrera", "Fecha Ingreso"]
            rows = []
            for carrera in carreras:
                if carrera.nombre == career.replace("-", " "):
                    rows = carrera.getList2()

    return jsonify({"status": "ok", "data": { "cols": cols, "rows": rows }}), 200

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')