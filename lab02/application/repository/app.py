from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import sql

URL_DB = "postgresql://lab2_db_fzi8_user:wR9gNQJA64ddrq7zz2mDmtiV4PzfhwaF@dpg-cucpojan91rc73ejbcug-a.ohio-postgres.render.com/lab2_db_fzi8"
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/tables/<table>', methods=['GET'])
def getTable(table):
    try:
        print("CONNECTOR: SOLICITUD RECIBIDA")
        conn = psycopg2.connect(URL_DB)
        cur = conn.cursor()
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table))
        cur.execute(query)
        rows = cur.fetchall()
        rows = [list(row) for row in rows]
        cur.close()
        conn.close()

        return jsonify({"status": "ok", "data": rows}), 200

    except psycopg2.Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')