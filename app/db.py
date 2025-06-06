import psycopg2
import psycopg2.extras

def get_db_connection():
    conn = psycopg2.connect(
        host='postgres',      # Use 'postgres' if running in Docker/Kubernetes
        database='postgres',
        user='postgres',
        password='postgres'
    )
    return conn 

