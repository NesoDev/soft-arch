import sqlite3
import csv

def f2(db_path):
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
    {"code": "10", "name": "Arquitectura Paisajística", "date": "2000-06-11", "description": "Diseño y planificación de espacios al aire libre."}
]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TCarreraProfesional(
        codigoCP INTEGER PRIMARY KEY AUTOINCREMENT,
        nomCP TEXT,
        fecha_creacion TEXT,
        observaciones TEXT
    )
    """)

        
    for school in UNMSM_SCHOOLS:
        cursor.execute("""
        INSERT INTO TCarreraProfesional (nomCP, fecha_creacion, observaciones)
        VALUES (?, ?, ?)
        """, (
            school["name"],
            school["date"],
            school["description"],
        ))
    
    conn.commit()
    conn.close()
    print("Datos insertados correctamente.")


def create_and_fill_table(csv_path, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TAlumno (
        codigo_alumno INTEGER PRIMARY KEY AUTOINCREMENT,
        ap TEXT,
        nom TEXT,
        edad INTEGER,
        sexo TEXT,
        peso REAL,
        talla REAL,
        color TEXT,
        prov TEXT,
        cod_cp TEXT,
        fecha_ingreso_U TEXT
    )
    """)
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute("""
            INSERT INTO TAlumno (ap, Nom, edad, sexo, peso, talla, color, prov, cod_cp, fecha_ingreso_U)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["Last Name"],
                row["First Name"],
                int(row["Age"]),
                row["Gender"],
                float(row["Weight"]),
                float(row["Height"]),
                row["Color"],
                row["Province"],
                row["School"],
                row["Admission Date"]
            ))
    
    conn.commit()
    conn.close()
    print("Datos insertados correctamente.")

if __name__ == "__main__":
    # Uso del script
    csv_path = "../lab01/profiles.csv"  # Cambia por el path correcto de tu archivo CSV
    db_path = "universidad.db"  # Base de datos SQLite donde se almacenarán los datos
    #create_and_fill_table(csv_path, db_path)

    #f2(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    #rows = cursor.execute("""
    #SELECT * FROM TAlumno
    #""")
    rows = cursor.execute("""
    SELECT * FROM TCarreraProfesional
    """)

    for row in rows:
        print(row)

    conn.close()