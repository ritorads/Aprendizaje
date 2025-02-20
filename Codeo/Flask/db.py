import psycopg2

def conexion_open_psqlFlask():
    try:
        conn = psycopg2.connect(
            dbname="psqlFlask",
            user="postgres",
            password="0",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None, None

def conexion_close_psqlFlask(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
