from datetime import datetime

class CarreraProfesional:
    def __init__ (self, codigo, nombre, fecha, descripcion, alumnos):
        self.codigo = codigo
        self.nombre = nombre
        self.fecha = fecha
        self.descripcion = descripcion
        self.alumnos = [alumno for alumno in alumnos if alumno.codigo_carrera == str(codigo)]
        self.cantidad_alumnos = len(self.alumnos)

    def getList1(self):
        return [self.codigo, self.nombre, self.fecha, self.descripcion, self.cantidad_alumnos]
    
    def getList2(self):
        fecha_limite = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
        condicion1 = [alumno for alumno in self.alumnos if datetime.strptime(alumno.fecha_ingreso, "%a, %d %b %Y %H:%M:%S %Z").date() > fecha_limite]
        condicion2 = [alumno for alumno in condicion1 if alumno.color.count("Rojo") == 0]
        condicion3 = [alumno for alumno in condicion2 if alumno.edad in range(18, 26)]
        return [alumno.getList() for alumno in condicion3]
    
class Alumno:
    def __init__(self, codigo, apellidos, nombres, edad, sexo, peso, talla, color, provincia, codigo_carrera, fecha_ingreso):
        self.codigo = codigo
        self.nombres = nombres
        self.apellidos = apellidos
        self.edad = edad
        self.sexo = sexo
        self.peso = peso
        self.talla = talla
        self.color = color
        self.provincia = provincia
        self.codigo_carrera = codigo_carrera
        self.fecha_ingreso = fecha_ingreso

    def getList(self):
        return [self.codigo, self.nombres, self.apellidos, self.edad, self.sexo, self.peso, self.talla, self.color, self.provincia, self.codigo_carrera, self.fecha_ingreso]