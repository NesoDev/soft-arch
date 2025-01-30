import requests
from application.db.models import Alumno, CarreraProfesional

URL_REPOSITORY = "http://127.0.0.1:3001/"

class Service:
    def get_list(self, number, career):
        print("BACKEND: SOLICITUD RECIBIDA")
        
        res = requests.get(URL_REPOSITORY + 'tables/talumno')
        data = res.json()
        print("DATA alumno RECIBIDA")
        
        alumnos = [Alumno(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]) for row in data["data"]]

        res = requests.get(URL_REPOSITORY + 'tables/tcarreraprofesional')
        data = res.json()
        print("DATA carrera RECIBIDA")
        
        carreras = [CarreraProfesional(carrera[0], carrera[1], carrera[2], carrera[3], alumnos) for carrera in data['data']]
        
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
        
        return {"status": "ok", "data": {"cols": cols, "rows": rows}}