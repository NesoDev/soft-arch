from datetime import datetime, timedelta
import random
import requests
import csv
from itertools import product
from concurrent.futures import ThreadPoolExecutor

PERU_PROVINCES = [
    "Lima", "Cusco", "Arequipa", "Trujillo", "Piura", "Chiclayo", "Tacna", 
    "Huancayo", "Iquitos", "Pucallpa", "Chimbote", "Juliaca", "Cajamarca", 
    "Huaraz", "Puno", "Huánuco", "Moquegua", "Tumbes", "Lambayeque", "Apurímac", 
    "Ayacucho", "Ucayali", "Loreto", "Junín", "Pasco", "San Martín", "Ancash", 
    "Callao", "San Juan de Lurigancho", "Chanchamayo", "Sechura", "Andahuaylas", 
    "Barranca", "Bagua", "Carhuaz", "Cañete", "Chota", "Comas", "Concepción", 
    "Chachapoyas", "Huancavelica", "Huaylas", "Huaral", "Jauja", "Jaén", "Ica", 
    "Huarmey", "Lima Provincias", "Loreto", "Moyobamba", "Pangoa", "Pataz", 
    "Puno", "Quillabamba", "Sicuani", "Satipo", "Sullana", "Tarma", "Tingo María", 
    "Tumbes", "Virú", "Zarumilla"
]

UNMSM_SCHOOLS = [
    {"code": "1", "name": "Ingeniería de Sistemas", "date": "1968-01-01", "description": "Pionera en tecnología e innovación."},
    {"code": "2", "name": "Medicina Humana", "date": "1856-05-12", "description": "Primera facultad de medicina en el país."},
    {"code": "3", "name": "Derecho", "date": "1821-07-28", "description": "Fundada durante la independencia."},
    {"code": "4", "name": "Economía", "date": "1950-03-15", "description": "Reconocida por su enfoque en desarrollo económico."},
    {"code": "5", "name": "Administración", "date": "1960-06-01", "description": "Facultad líder en gestión empresarial."},
    {"code": "6", "name": "Matemáticas", "date": "1940-08-18", "description": "Enfocada en matemáticas puras y aplicadas."},
    {"code": "7", "name": "Física", "date": "1935-10-01", "description": "Cuenta con laboratorios de última generación."},
    {"code": "8", "name": "Ciencias Sociales", "date": "1970-02-01", "description": "Promueve la investigación interdisciplinaria."},
    {"code": "9", "name": "Psicología", "date": "1965-11-20", "description": "Ofrece especialización en varias áreas clínicas."},
    {"code": "10", "name": "Química", "date": "1925-04-15", "description": "Cuenta con amplia experiencia en investigación química."},
    {"code": "11", "name": "Historia", "date": "1920-03-10", "description": "Fomenta el análisis crítico de los procesos históricos."},
    {"code": "12", "name": "Ingeniería Industrial", "date": "1975-07-15", "description": "Alta empleabilidad en el sector manufacturero."},
    {"code": "13", "name": "Arquitectura", "date": "1955-09-01", "description": "Famosa por sus proyectos de diseño urbano."},
    {"code": "14", "name": "Biología", "date": "1947-11-22", "description": "Enfoque en biodiversidad y ecología."},
    {"code": "15", "name": "Ciencias de la Comunicación", "date": "1980-06-15", "description": "Reconocida en medios de comunicación nacionales."},
    {"code": "16", "name": "Antropología", "date": "1968-10-01", "description": "Enfocada en el estudio de culturas y sociedades."},
    {"code": "17", "name": "Educación", "date": "1925-04-10", "description": "Facultad clave en formación docente."},
    {"code": "18", "name": "Geografía", "date": "1945-01-12", "description": "Especializada en análisis geoespacial."},
    {"code": "19", "name": "Odontología", "date": "1950-06-10", "description": "Ofrece clínicas para atención al público."},
    {"code": "20", "name": "Arte", "date": "1930-07-20", "description": "Enseña diversas disciplinas artísticas."},
    {"code": "21", "name": "Tecnología Médica", "date": "1975-09-05", "description": "Formación técnica en equipos médicos."},
    {"code": "22", "name": "Enfermería", "date": "1940-11-15", "description": "Primera escuela de enfermería del Perú."},
    {"code": "23", "name": "Farmacia y Bioquímica", "date": "1918-03-08", "description": "Contribuye a la investigación farmacológica."},
    {"code": "24", "name": "Veterinaria", "date": "1952-08-18", "description": "Promueve el cuidado de la salud animal."},
    {"code": "25", "name": "Zootecnia", "date": "1960-05-01", "description": "Especialización en producción animal sostenible."},
    {"code": "26", "name": "Ingeniería Química", "date": "1968-03-01", "description": "Formación en procesos industriales y sostenibilidad."},
    {"code": "27", "name": "Ingeniería Civil", "date": "1920-08-10", "description": "Focalizada en la construcción y diseño de infraestructuras."},
    {"code": "28", "name": "Ingeniería Agrícola", "date": "1973-09-15", "description": "Especialización en el uso de la tecnología para la agricultura."},
    {"code": "29", "name": "Ingeniería Mecánica", "date": "1960-07-20", "description": "Enfoque en sistemas y maquinaria industrial."},
    {"code": "30", "name": "Ingeniería Electrónica", "date": "1965-05-15", "description": "Famosa por su formación en circuitos y comunicaciones."},
    {"code": "31", "name": "Ingeniería Ambiental", "date": "1990-02-01", "description": "Enfoque en soluciones para la sostenibilidad."},
    {"code": "32", "name": "Ingeniería Agrónoma", "date": "1960-08-10", "description": "Formación en la producción agrícola sostenible."},
    {"code": "33", "name": "Tecnología en Alimentos", "date": "1995-06-01", "description": "Formación enfocada en la industria alimentaria."},
    {"code": "34", "name": "Genética y Biotecnología", "date": "1992-04-22", "description": "Enfoque en la manipulación genética y su aplicación."},
    {"code": "35", "name": "Filosofía", "date": "1910-11-15", "description": "Promueve el análisis crítico y la reflexión."},
    {"code": "36", "name": "Sociología", "date": "1950-03-01", "description": "Estudia la estructura de la sociedad y los problemas sociales."},
    {"code": "37", "name": "Arqueología", "date": "1965-07-01", "description": "Enfoque en el estudio de las civilizaciones antiguas."},
    {"code": "38", "name": "Lingüística", "date": "1940-05-20", "description": "Fomenta el estudio de lenguas y su estructura."},
    {"code": "39", "name": "Literatura", "date": "1920-06-01", "description": "Enseña sobre la interpretación y análisis literario."},
    {"code": "40", "name": "Ciencias Políticas", "date": "1960-03-15", "description": "Formación en teoría política y administración pública."},
    {"code": "41", "name": "Relaciones Internacionales", "date": "1990-09-10", "description": "Estudia la interacción entre países y culturas."},
    {"code": "42", "name": "Geología", "date": "1945-11-01", "description": "Famosa por su formación en estudios geológicos."},
    {"code": "43", "name": "Ingeniería de Minas", "date": "1965-04-22", "description": "Focalizada en la explotación y procesamiento de recursos mineros."},
    {"code": "44", "name": "Ingeniería de Materiales", "date": "1975-08-15", "description": "Formación en investigación y diseño de nuevos materiales."},
    {"code": "45", "name": "Estadística", "date": "1960-05-30", "description": "Especializada en el análisis de datos y probabilidades."},
    {"code": "46", "name": "Ingeniería de Software", "date": "1995-11-22", "description": "Formación en desarrollo y diseño de software."},
    {"code": "47", "name": "Ingeniería en Telecomunicaciones", "date": "1965-09-01", "description": "Focalizada en sistemas de comunicación a distancia."},
    {"code": "48", "name": "Ingeniería en Energía", "date": "1990-01-10", "description": "Enfoque en la optimización de recursos energéticos."},
    {"code": "49", "name": "Ingeniería de Petróleos", "date": "1985-06-10", "description": "Formación en la industria del petróleo y gas."},
    {"code": "50", "name": "Ingeniería Agroindustrial", "date": "1980-03-15", "description": "Enfocada en el procesamiento de productos agrícolas."},
    {"code": "51", "name": "Ingeniería Forestal", "date": "1975-07-01", "description": "Fomenta la conservación de bosques y ecosistemas."},
    {"code": "52", "name": "Biotecnología", "date": "2000-09-01", "description": "Enfoque en la investigación de aplicaciones biotecnológicas."},
    {"code": "53", "name": "Ciencias del Mar", "date": "1995-04-22", "description": "Formación en el estudio de los océanos y sus recursos."},
    {"code": "54", "name": "Ciencias del Deporte", "date": "1985-12-05", "description": "Fomentando el estudio y la práctica del deporte."},
    {"code": "55", "name": "Tecnologías de la Información", "date": "2000-01-15", "description": "Formación en el uso y desarrollo de tecnologías de la información."},
    {"code": "56", "name": "Investigación Criminal", "date": "2005-07-10", "description": "Enfoque en técnicas de investigación y criminología."},
    {"code": "57", "name": "Seguridad Ciudadana", "date": "2010-06-01", "description": "Focalizada en la gestión de seguridad pública."},
    {"code": "58", "name": "Diseño Gráfico", "date": "1995-11-20", "description": "Formación en creación visual para diversos medios."},
    {"code": "59", "name": "Marketing", "date": "1990-03-01", "description": "Enfoque en estrategias comerciales y de mercado."},
    {"code": "60", "name": "Publicidad", "date": "1985-09-01", "description": "Enseñanza de comunicación y campañas publicitarias."},
    {"code": "61", "name": "Gestión Cultural", "date": "2000-07-15", "description": "Fomento de proyectos culturales y artísticos."},
    {"code": "62", "name": "Ingeniería de Energía Renovable", "date": "2015-05-01", "description": "Formación en soluciones energéticas sostenibles."},
    {"code": "63", "name": "Ciencias Forenses", "date": "2000-10-10", "description": "Especialización en investigación criminal y pruebas."},
    {"code": "64", "name": "Diseño Industrial", "date": "1980-02-01", "description": "Formación en diseño de productos industriales."},
    {"code": "65", "name": "Ingeniería Biomédica", "date": "1995-08-20", "description": "Formación en la intersección de la ingeniería y la medicina."},
    {"code": "66", "name": "Ingeniería Mecatrónica", "date": "2005-09-05", "description": "Enfoque en la combinación de electrónica y mecánica."},
    {"code": "67", "name": "Ingeniería de Tránsito", "date": "2010-04-15", "description": "Estudia la planificación de sistemas de transporte."},
    {"code": "68", "name": "Ciencias del Clima", "date": "2015-01-20", "description": "Formación en el estudio y modelado del clima."},
    {"code": "69", "name": "Antropología Social", "date": "1980-12-05", "description": "Estudia las prácticas sociales y culturales."},
    {"code": "70", "name": "Ciencias de la Información", "date": "2000-11-30", "description": "Formación en la gestión y análisis de información."},
    {"code": "71", "name": "Gestión de la Innovación", "date": "2010-06-20", "description": "Enfoque en la innovación tecnológica y empresarial."},
    {"code": "72", "name": "Gestión de la Salud", "date": "2005-03-01", "description": "Fomento de la gestión de recursos en salud pública."},
    {"code": "73", "name": "Gestión de Proyectos", "date": "2015-06-10", "description": "Enfoque en la planificación y ejecución de proyectos."},
    {"code": "74", "name": "Ingeniería Aeroespacial", "date": "2015-09-01", "description": "Formación en diseño y producción de aeronaves."},
    {"code": "75", "name": "Ingeniería de Software Avanzado", "date": "2015-07-05", "description": "Formación en desarrollo de software de alto nivel."},
    {"code": "76", "name": "Ingeniería en Telecomunicaciones Avanzada", "date": "2010-10-15", "description": "Enfoque en redes avanzadas y telecomunicaciones."},
    {"code": "77", "name": "Computación Cuántica", "date": "2020-01-10", "description": "Formación en las nuevas tecnologías cuánticas."},
    {"code": "78", "name": "Big Data", "date": "2020-07-01", "description": "Formación en análisis y procesamiento de grandes datos."},
    {"code": "79", "name": "Neurociencia", "date": "2015-12-15", "description": "Estudio de las ciencias cognitivas y del cerebro."},
    {"code": "80", "name": "Ciencias de la Computación", "date": "1995-09-10", "description": "Formación en algoritmos, estructuras y programación."},
    {"code": "81", "name": "Investigación en Inteligencia Artificial", "date": "2020-08-10", "description": "Estudio de aplicaciones y modelos en IA."},
    {"code": "82", "name": "Ingeniería de Proyectos", "date": "2000-04-01", "description": "Especialización en la gestión efectiva de proyectos."},
    {"code": "83", "name": "Gestión del Conocimiento", "date": "2010-09-25", "description": "Fomento de la gestión de información en organizaciones."},
    {"code": "84", "name": "Ciberseguridad", "date": "2015-01-15", "description": "Formación en protección de sistemas informáticos."},
    {"code": "85", "name": "Ingeniería de Datos", "date": "2020-09-05", "description": "Enfoque en el análisis y manejo de grandes volúmenes de datos."},
    {"code": "86", "name": "Ingeniería en Robótica", "date": "2015-06-30", "description": "Estudio de la creación y control de robots."},
    {"code": "87", "name": "Ciencias de la Salud", "date": "2005-03-05", "description": "Formación en salud pública y medicina general."},
    {"code": "88", "name": "Ciencias del Trabajo", "date": "1990-02-15", "description": "Estudio de las relaciones laborales y derechos."},
    {"code": "89", "name": "Gestión de la Calidad", "date": "2005-11-30", "description": "Fomento de técnicas de control de calidad en procesos."},
    {"code": "90", "name": "Tecnologías Emergentes", "date": "2015-10-01", "description": "Estudio de las nuevas tecnologías y su impacto."},
    {"code": "91", "name": "Mecánica Computacional", "date": "2015-01-25", "description": "Estudio de la simulación numérica y métodos computacionales."},
    {"code": "92", "name": "Gestión Ambiental", "date": "2005-12-15", "description": "Estudio de la gestión sostenible de recursos naturales."},
    {"code": "93", "name": "Comercio Internacional", "date": "2010-05-10", "description": "Formación en gestión de mercados globales."},
    {"code": "94", "name": "Ingeniería de la Producción", "date": "2015-08-25", "description": "Fomento de la producción eficiente en la industria."},
    {"code": "95", "name": "Ingeniería Biomédica Aplicada", "date": "2015-02-20", "description": "Enfoque en tecnologías biomédicas aplicadas a la medicina."},
    {"code": "96", "name": "Ciencias Ambientales", "date": "2005-07-10", "description": "Estudio del impacto humano en el medio ambiente."},
    {"code": "97", "name": "Tecnología de la Información en la Nube", "date": "2020-03-01", "description": "Formación en almacenamiento y procesamiento en la nube."},
    {"code": "98", "name": "Ingeniería de Videojuegos", "date": "2015-04-10", "description": "Formación en diseño y desarrollo de videojuegos."},
    {"code": "99", "name": "Emprendimiento Social", "date": "2010-07-20", "description": "Fomento de proyectos emprendedores con impacto social."},
    {"code": "100", "name": "Gestión Financiera", "date": "2015-11-30", "description": "Formación en la administración y control de recursos financieros."},
    {"code": "101", "name": "Mantenimiento Industrial", "date": "2000-04-05", "description": "Formación técnica en mantenimiento de maquinaria industrial."},
    {"code": "102", "name": "Diseño de Interiores", "date": "1990-06-15", "description": "Formación en diseño y decoración de espacios interiores."},
    {"code": "103", "name": "Administración Pública", "date": "2000-09-10", "description": "Estudio de la gestión del sector público."},
    {"code": "104", "name": "Ingeniería Geográfica", "date": "2015-07-25", "description": "Estudio de los procesos y sistemas geográficos."},
    {"code": "105", "name": "Ciencias Matemáticas", "date": "2005-04-10", "description": "Formación en teoría y prácticas matemáticas avanzadas."},
    {"code": "106", "name": "Desarrollo Urbano", "date": "2010-03-05", "description": "Estudio de la planificación y expansión de ciudades."},
    {"code": "107", "name": "Gestión de la Salud Pública", "date": "2005-02-15", "description": "Enfoque en políticas de salud pública."},
    {"code": "108", "name": "Gestión Tecnológica", "date": "2015-05-20", "description": "Formación en la integración de la tecnología en los negocios."},
    {"code": "109", "name": "Administración de Empresas", "date": "1990-05-01", "description": "Formación en gestión y administración de empresas."},
    {"code": "110", "name": "Sistemas de Información", "date": "2005-10-05", "description": "Formación en el desarrollo y gestión de sistemas de información."},
    {"code": "111", "name": "Mercadotecnia Internacional", "date": "2000-01-05", "description": "Estudio de estrategias comerciales a nivel global."},
    {"code": "112", "name": "Ingeniería de Gestión", "date": "2015-06-30", "description": "Formación en gestión empresarial."},
    {"code": "113", "name": "Ingeniería en Diseño de Producto", "date": "2015-11-15", "description": "Focalizada en el diseño y creación de productos industriales."},
    {"code": "114", "name": "Diseño de Moda", "date": "2005-07-01", "description": "Formación en la creación de ropa y accesorios."},
    {"code": "115", "name": "Estudios Internacionales", "date": "2010-01-20", "description": "Formación en relaciones y estudios internacionales."},
    {"code": "116", "name": "Ciencias de la Ingeniería", "date": "2000-03-30", "description": "Estudio general de las ramas de ingeniería."},
    {"code": "117", "name": "Ingeniería de Control", "date": "2015-01-10", "description": "Formación en el control de sistemas industriales."},
    {"code": "118", "name": "Ciencias del Lenguaje", "date": "1990-08-05", "description": "Estudio de la lengua, literatura y comunicación."},
    {"code": "119", "name": "Ciencias Sociales", "date": "1985-06-15", "description": "Estudio de la sociedad y las relaciones humanas."},
    {"code": "120", "name": "Ingeniería de Materiales", "date": "2005-11-10", "description": "Estudio de los materiales y sus aplicaciones industriales."}
]

COLORS = [
    "Negro", "Marrón", "Verde", "Azul", "Púrpura", "Violeta", "Azul Cielo",
    "Rojo", "Naranja", "Amarillo", "Rosa", "Gris", "Blanco", "Beige", "Turquesa",
    "Aqua", "Lila", "Mostaza", "Salmón", "Coral", "Lavanda", "Verde Oliva", 
    "Verde Esmeralda", "Azul Marino", "Azul Claro", "Azul Turquesa", "Menta", 
    "Perla", "Cobre", "Plata", "Oro", "Fucsia", "Vino", "Naranja Quemado", "Índigo", 
    "Esmeralda", "Zafiro", "Oliva", "Paja", "Chocolate", "Ciruela", "Champán", 
    "Caramelo", "Verde Lima", "Mandarina", "Gris Oscuro", "Gris Claro", "Verde Bosque", 
    "Amarillo Mostaza", "Rosa Pastel", "Verde Pastel", "Azul Pastel", "Naranja Pastel", 
    "Rosa Fuerte", "Rojo Vivo", "Azul Eléctrico", "Azul Acero", "Cian", "Aguamarina", 
    "Verde Menta", "Turquesa Claro", "Púrpura Claro", "Vino Claro", "Naranja Claro", 
    "Rosa Claro", "Amarillo Claro", "Ocre", "Lavanda Claro", "Café", "Granate", 
    "Siena", "Azul Petróleo", "Verde Mar", "Rosa Fucsia", "Malva", "Salmón Claro", 
    "Azul Zafiro", "Marrón Claro", "Marrón Oscuro", "Blanco Roto", "Verde Lima Claro", 
    "Rojo Coral", "Café Claro", "Lima", "Amarillo Oro", "Oro Claro", "Beige Claro", 
    "Azul Acero Claro", "Verde Pasto", "Verde Oliva Claro", "Verde Lima Oscuro", 
    "Lavanda Oscuro", "Rosa Pálido", "Blanco Perla", "Beige Oscuro", "Naranja Brillante", 
    "Rojo Oscuro", "Amarillo Canario", "Púrpura Oscuro", "Rosa Barbie", "Azul Ultramar",
    "Gris Pálido", "Azul Verdoso", "Rojo Frambuesa", "Cyan Claro", "Cielo Azul", 
    "Verde Bosque Claro", "Fucsia Claro", "Turquesa Oscuro", "Azul Claro Pastel", 
    "Caramelo Claro", "Gris Azulado", "Verde Limón", "Naranja Mandarina", "Pardo", 
    "Rosa Químico", "Oro Rosa", "Marfil", "Naranja Intenso", "Rojo Burdeos", "Perla Claro", 
    "Gris Pizarra", "Marino", "Azul Grisáceo", "Turquesa Oscuro", "Azul Claro Pastel", 
    "Verde Pastel Claro", "Rosa Pálido Claro", "Amarillo Cálido", "Piedra", 
    "Verde Peppermint", "Dorado Claro", "Marrón Aceituna", "Gris Tiza", "Gris Carbón", 
    "Ocre Claro", "Burlwood", "Azul Tiza", "Verde Agave", "Azul Claro Eléctrico", 
    "Azul Polvo", "Rojo Coral Claro", "Magenta", "Rojo Girasol", "Verde Manzana", 
    "Verde Oliva Oscuro", "Verde Militar", "Verde Pasto Claro", "Gris Silencio", 
    "Naranja Papaya", "Amarillo Mostaza Claro", "Marrón Tostado", "Azul Tintado", 
    "Beige Roso", "Vino Oscuro", "Ámbar Oscuro", "Verde Romero", "Cian Claro", 
    "Marrón Caoba", "Amarillo Limón", "Salmón Rosa", "Madera", "Gris Oscuro Claro", 
    "Amanecer", "Miel Claro", "Caramelo Oscuro", "Rosa Flamingo", "Cerezo", "Carmesí", 
    "Gris Beto", "Verde Albahaca", "Azul Medianoche", "Azul Turquesa Claro", "Terracota", 
    "Verde Cacto", "Plata Claro", "Piedra Gris", "Fucsia Oscuro", "Verde Azulado", 
    "Oro Viejo", "Azul Plomo", "Café Intenso", "Gris Claro Plateado", "Naranja Fósforo", 
    "Verde Alga", "Rojo Polvo", "Blanco Ártico", "Verde Genciana", "Rosa Mandarina", 
    "Rojo Maíz", "Azul Espuma", "Verde Primavera", "Azul Volcánico", "Verde Rúcula", 
    "Carmín", "Piedra Natural", "Lavanda Gris", "Amarillo Sol", "Piedra Gris Claro", 
    "Plata Metálico", "Rojo Cereza", "Verde Claro Pastel", "Amarillo Arcilla"
]

def get_first_last_names(count):
    url = f"https://randomuser.me/api/?results={count}"
    response = requests.get(url)
    data = response.json()
    first_names = [user["name"]["first"] for user in data["results"] if user["name"]["first"].isalpha()]
    last_names = [user["name"]["last"] for user in data["results"] if user["name"]["last"].isalpha()]
    return first_names, last_names

def generate_profiles(first_names, last_names, profile_count):
    profiles = []
    profiles_generated = 0
    def generate_batch(first_name, last_names):
        nonlocal profiles_generated
        batch_profiles = []
        for last_name1, last_name2 in product(last_names, repeat=2):
            batch_profiles.append(generate_profile(first_name, last_name1, last_name2))
            profiles_generated += 1
            progress = (profiles_generated / profile_count) * 100
            print(f"Progress: {progress:.2f}%", end="\r")
            if len(batch_profiles) >= profile_count // len(first_names):
                break
        return batch_profiles
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(generate_batch, first_name, last_names) for first_name in first_names]
        for future in futures:
            profiles.extend(future.result())
    print()
    return profiles

def generate_profile(first_name, last_name1, last_name2):
    gender = random.choice(["Male", "Female"])
    age = random.randint(18, 30)
    weight = round(random.uniform(50, 90), 1)
    height = round(random.uniform(1.5, 2.0), 2)
    color = random.choice(COLORS)
    province = random.choice(PERU_PROVINCES)
    school_dict = random.choice(UNMSM_SCHOOLS)
    code_school = school_dict["code"]
    admission_date = datetime.now() - timedelta(days=random.randint(1, 365 * 5))
    admission_date = admission_date.strftime("%Y-%m-%d")
    return [f"{last_name1} {last_name2}", first_name, age, gender, weight, height, color, province, code_school, admission_date]

def save_to_csv(profiles, filename="profiles.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Last Name", "First Name", "Age", "Gender", "Weight", "Height", "Color", "Province", "School", "Admission Date"])
        for profile in profiles:
            writer.writerow(profile)
    print(f"Profiles saved to {filename}")

if __name__ == "__main__":
    profile_count = 200_000
    first_names, last_names = get_first_last_names(1000)
    print(f"Retrieved {len(first_names)} first names and {len(last_names)} last names")
    print(f"Generating {profile_count} profiles...")
    profiles = generate_profiles(first_names, last_names, profile_count)
    print(f"Generated {len(profiles)} profiles")
    save_to_csv(profiles)