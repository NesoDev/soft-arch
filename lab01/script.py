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
    {"code": "50", "name": "Ingeniería Agroindustrial", "date": "1980-07-10", "description": "Enfoque en la industrialización de productos agrícolas."},
    {"code": "51", "name": "Teología", "date": "1960-09-05", "description": "Enfoque en el estudio de las religiones y la espiritualidad."},
    {"code": "52", "name": "Ingeniería de Transporte", "date": "1995-02-15", "description": "Formación en sistemas de transporte y logística."},
    {"code": "53", "name": "Diseño Gráfico", "date": "1980-05-20", "description": "Desarrollo de habilidades en el diseño visual y la comunicación."},
    {"code": "54", "name": "Terapia Física", "date": "1980-11-10", "description": "Formación en rehabilitación física y tratamiento de lesiones."},
    {"code": "55", "name": "Derecho Notarial y Registral", "date": "1992-04-18", "description": "Especialización en la normativa de registros públicos."},
    {"code": "56", "name": "Nutrición", "date": "1965-02-01", "description": "Formación en salud alimentaria y dietética."},
    {"code": "57", "name": "Trabajo Social", "date": "1950-06-12", "description": "Enfocada en la mejora del bienestar social y comunitario."},
    {"code": "58", "name": "Gestión Cultural", "date": "1990-08-22", "description": "Enfoque en la administración de proyectos culturales."},
    {"code": "59", "name": "Ingeniería Agrónoma", "date": "1960-08-05", "description": "Formación en la gestión agrícola sostenible y responsable."},
    {"code": "60", "name": "Diseño de Moda", "date": "1990-11-15", "description": "Especialización en la creación de ropa y tendencias."},
    {"code": "61", "name": "Educación Física", "date": "1970-03-12", "description": "Formación en deportes y promoción de la salud."},
    {"code": "62", "name": "Ciencias de la Información", "date": "1985-06-28", "description": "Enfoque en el manejo y análisis de información."},
    {"code": "63", "name": "Cine y Producción Audiovisual", "date": "2000-03-15", "description": "Formación en la producción y dirección cinematográfica."},
    {"code": "64", "name": "Música", "date": "1935-10-01", "description": "Especialización en la interpretación y teoría musical."},
    {"code": "65", "name": "Ingeniería Forestal", "date": "1978-06-12", "description": "Enfoque en la gestión de recursos forestales."},
    {"code": "66", "name": "Ingeniería Geográfica", "date": "1995-07-18", "description": "Formación en el análisis espacial y geoespacial."},
    {"code": "67", "name": "Ingeniería de Diseño Industrial", "date": "1990-09-01", "description": "Especialización en la creación y diseño de productos industriales."},
    {"code": "68", "name": "Ciencias de la Educación Infantil", "date": "1980-09-20", "description": "Formación para la enseñanza y el desarrollo infantil."},
    {"code": "69", "name": "Terapia Ocupacional", "date": "1975-11-10", "description": "Formación en rehabilitación a través de actividades diarias."},
    {"code": "70", "name": "Ingeniería de Seguridad y Salud en el Trabajo", "date": "2000-10-05", "description": "Enfoque en la prevención de riesgos laborales."},
    {"code": "71", "name": "Estudios Internacionales", "date": "1990-12-22", "description": "Formación en relaciones y políticas internacionales."},
    {"code": "72", "name": "Ingeniería en Biotecnología", "date": "1995-03-08", "description": "Especialización en el uso de organismos vivos en procesos industriales."},
    {"code": "73", "name": "Fisioterapia", "date": "1980-05-30", "description": "Formación en rehabilitación y tratamiento físico."},
    {"code": "74", "name": "Ciencias Ambientales", "date": "1990-04-01", "description": "Enfoque en la conservación del medio ambiente."},
    {"code": "75", "name": "Ingeniería de Energía Renovable", "date": "2005-01-18", "description": "Formación en el aprovechamiento de fuentes energéticas alternativas."},
    {"code": "76", "name": "Diseño de Videojuegos", "date": "2005-06-10", "description": "Formación en el diseño y desarrollo de videojuegos."},
    {"code": "77", "name": "Periodismo", "date": "1965-08-12", "description": "Enfoque en la creación de contenido y comunicación de noticias."},
    {"code": "78", "name": "Ingeniería Biomédica", "date": "1992-03-05", "description": "Especialización en la ingeniería de equipos médicos."},
    {"code": "79", "name": "Publicidad y Marketing", "date": "1985-10-15", "description": "Formación en la promoción y comercialización de productos."},
    {"code": "80", "name": "Ciencias Forenses", "date": "1998-11-20", "description": "Estudio de los aspectos científicos aplicados al derecho."},
    {"code": "81", "name": "Mantenimiento Industrial", "date": "1980-03-12", "description": "Formación en la reparación y mantenimiento de equipos industriales."},
    {"code": "82", "name": "Ingeniería en Sistemas de Información", "date": "1990-04-25", "description": "Enfoque en el desarrollo y gestión de sistemas informáticos."},
    {"code": "83", "name": "Trabajo de Campo", "date": "2000-05-02", "description": "Estudios prácticos para investigación científica."},
    {"code": "84", "name": "Ciencia Política", "date": "1968-12-05", "description": "Formación en teoría y práctica política."},
    {"code": "85", "name": "Estudios Asiáticos", "date": "1995-10-22", "description": "Estudios sobre la cultura, historia y política de Asia."},
    {"code": "86", "name": "Antropología Forense", "date": "2000-06-15", "description": "Estudio de restos humanos para la resolución de casos legales."},
    {"code": "87", "name": "Ingeniería en Inteligencia Artificial", "date": "2005-09-01", "description": "Formación en el desarrollo de sistemas inteligentes."},
    {"code": "88", "name": "Arte Dramático", "date": "1965-08-25", "description": "Formación en actuación y producción teatral."},
    {"code": "89", "name": "Relaciones Públicas", "date": "1980-10-01", "description": "Enfoque en la comunicación organizacional."},
    {"code": "90", "name": "Mecánica Automotriz", "date": "1970-03-25", "description": "Especialización en reparación y mantenimiento de vehículos."},
    {"code": "91", "name": "Producción de Eventos", "date": "1995-07-22", "description": "Formación en la planificación y gestión de eventos."},
    {"code": "92", "name": "Ingeniería en Robótica", "date": "2010-11-02", "description": "Formación en el diseño y programación de robots."},
    {"code": "93", "name": "Educación Parvularia", "date": "1985-04-10", "description": "Formación en el cuidado y desarrollo de niños pequeños."},
    {"code": "94", "name": "Ingeniería de Logística", "date": "2000-02-15", "description": "Focalizada en la gestión eficiente de la cadena de suministro."},
    {"code": "95", "name": "Ciencias de la Actividad Física", "date": "1995-06-01", "description": "Formación en la práctica y la gestión del deporte."},
    {"code": "96", "name": "Fisioterapia Respiratoria", "date": "1992-09-08", "description": "Enfoque en el tratamiento de enfermedades respiratorias."},
    {"code": "97", "name": "Ingeniería del Software y Redes", "date": "2005-08-20", "description": "Desarrollo de aplicaciones y gestión de redes de comunicación."},
    {"code": "98", "name": "Biología Marina", "date": "1985-11-01", "description": "Estudio de ecosistemas marinos y protección de especies acuáticas."},
    {"code": "99", "name": "Matemáticas Aplicadas", "date": "1990-05-01", "description": "Aplicación de teorías matemáticas a problemas prácticos."},
    {"code": "100", "name": "Arquitectura Paisajística", "date": "2000-06-11", "description": "Diseño y planificación de espacios al aire libre."}
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
    profile_count = 1_000_000
    first_names, last_names = get_first_last_names(1000)
    print(f"Retrieved {len(first_names)} first names and {len(last_names)} last names")
    print(f"Generating {profile_count} profiles...")
    profiles = generate_profiles(first_names, last_names, profile_count)
    print(f"Generated {len(profiles)} profiles")
    save_to_csv(profiles)