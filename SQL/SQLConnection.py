import psycopg2

# Schema
"""
Disease(disease_id, disease_name)
Symptom(symptom_id, symptom_name);
Has_Symptoms( disease_id , symptom_id)
"""

# Function to connect to PostgreSQL
def connect(db_name, db_password):
    try:
        connection = psycopg2.connect(
        dbname = db_name,
        user = "postgres",
        password = db_password,
        host = "localhost",
        port = "5432"
        )
        return connection
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(f"Error in connection to database: {e}")
        return None

# Function to get data from the table
# select {col_name} from {table_name}
def CallDB(table_name, col_name):
    try:
        conn = connect("medhat_db", "medhat123")
        cursor = conn.cursor()
        cursor.execute(f"SELECT {col_name} FROM {table_name}")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except psycopg2.Error as e:
        print("Error fetching data")
        print(e)
        return None
    
def QueryDB(query):
    try:
        conn = connect("medhat_db", "medhat123")
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except psycopg2.Error as e:
        print("Error fetching data")
        print(e)
        return None

# Connecting to the database
connection = connect("medhat_db", "medhat123")

if connection is not None:
    # Getting data (list of tuples "rows")
    #DiseasesDB = CallDB(connection,"disease","*")
    #SymptomsDB = CallDB(connection,"symptom","*")
    #Associated_SymptomsDB = CallDB(connection,"has_symptoms","*")
    # Closing the connection
    connection.close()
else:
    print("Connection to the database failed")
