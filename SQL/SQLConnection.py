import psycopg2

# Schema
"""
Disease(disease_id, disease_name)
Symptom(symptom_id, symptom_name);
Has_Symptoms( disease_id , symptom_id)
"""

# database name and password
DBname = "medhat_db"
DBpassword = "medhat123"

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
        conn = connect(DBname, DBpassword)
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
        conn = connect(DBname, DBpassword)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except psycopg2.Error as e:
        print("Error fetching data")
        print(e)
        return None

# function to create a database
def create_database(dbname, user, password, host, port):
    try:
        # Connect to the default 'postgres' database first
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Execute SQL command to create a new database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")

        cursor.close()
        conn.close()
        print(f"Database '{dbname}' created successfully")
    except psycopg2.Error as e:
        print("Error creating database")
        print(e)
    
# Function to create tables
def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE if not exists Disease( 
            disease_id SMALLINT PRIMARY KEY,
            disease_name VARCHAR(100) NOT NULL);

            CREATE TABLE if not exists Symptom( 
            symptom_id SMALLINT PRIMARY KEY,
            symptom_name VARCHAR(200) NOT NULL);

            CREATE TABLE if not exists Has_Symptoms(
            disease_id SMALLINT,
            symptom_id SMALLINT,
            primary key (disease_id,symptom_id),
            FOREIGN KEY (disease_id) REFERENCES Disease(disease_id),
            FOREIGN KEY (symptom_id) REFERENCES Symptom(symptom_id)
            ON DELETE CASCADE);
            """
        )
        connection.commit()
        cursor.close()

    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")

# function to copy data from a csv file to a table in a database
def csv_to_db(table_name, connection):
    try:
        # Create a cursor object
        cur = connection.cursor()

        # Path to your CSV file and table name
        csv_file = f'CSVs\{table_name}.csv'
        db_table_name = table_name

        # SQL COPY command to import the CSV file
        copy_sql = f"COPY {table_name} FROM stdin DELIMITER ',' CSV HEADER"
        with open(csv_file, 'r') as f:
            cur.copy_expert(sql=copy_sql, file=f)

        # Commit changes and close the connection
        connection.commit()
        cur.close()

    except psycopg2.Error as e:
        print(f"Error in transferring data from {table_name} csv file to the database: {e}")

def init_db(db_name, db_password):
    tables_list = ["disease", "symptom", "has_symptoms"]

    create_database(db_name, "postgres", db_password, "localhost", "5432")

    connection = connect(db_name, db_password)

    create_tables(connection)

    for table in tables_list:
        csv_to_db(table, connection)

    print("initialization of the database ended successfully!")

    connection.close()

# call the following before starting the chatbot inside Medhat.py
#init_db(DBname, DBpassword)
