import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    # Connect to the default postgres database to create the new one
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="Siddartha57",
            host="localhost",
            port="5432",
            dbname="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if momentum db exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'momentum'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE momentum")
            print("Database 'momentum' created successfully.")
        else:
            print("Database 'momentum' already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_db()
