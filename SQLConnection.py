import psycopg2

# DB Schema
"""
Diseases(disease_id, disease_name, description, treatments, causes, severity, specialist, frequency, contagiousness)
Symptoms(symptom_id, symptom_name);
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

def QueryDB(query, values=None, fetch=True):
    try:
        conn = connect(DBname, DBpassword)
        cursor = conn.cursor()

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        if fetch:
            rows = cursor.fetchall()
            result = []
            for row in rows:
                new_row = []
                for entry in row:
                    if isinstance(entry, str):
                        new_row.append(entry.rstrip())
                    else:
                        new_row.append(entry)
                result.append(new_row)
            return result
        else:
            # For non-SELECT queries (INSERT, UPDATE, DELETE)
            conn.commit()
            return None

    except psycopg2.Error as e:
        print("Error executing the query:", e)
        return None

    finally:
        cursor.close()
        conn.close()


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
            CREATE TABLE if not exists Diagnoses (
                diagnosis_id SERIAL PRIMARY KEY,
                disease_id SMALLINT,
                FOREIGN KEY (disease_id) REFERENCES Diseases(disease_id),
                d_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE if not exists Diseases( 
            disease_id SMALLINT PRIMARY KEY,
            disease_name NCHAR(70) NOT NULL,
            description NCHAR(275),
            treatments NCHAR(2400),
            causes NCHAR(2400),
            severity NCHAR(10),
            specialist NCHAR(75),
            frequency NCHAR(10),
            contagiousness NCHAR(5));

            CREATE TABLE if not exists Symptoms( 
            symptom_id SMALLINT PRIMARY KEY,
            symptom_name NCHAR(75) NOT NULL);

            CREATE TABLE if not exists Has_Symptoms(
            disease_id SMALLINT,
            symptom_id SMALLINT,
            primary key (disease_id,symptom_id),
            FOREIGN KEY (disease_id) REFERENCES Diseases(disease_id),
            FOREIGN KEY (symptom_id) REFERENCES Symptoms(symptom_id)
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
        csv_file = f'CSVs/{table_name}.csv'

        # SQL COPY command to import the CSV file
        copy_sql = f"COPY {table_name} FROM stdin DELIMITER ',' CSV HEADER"
        with open(csv_file, 'r') as f:
            cur.copy_expert(sql=copy_sql, file=f)

        # Commit changes
        connection.commit()

        # Close the cursor
        cur.close()

    except psycopg2.Error as e:
        # Print the error details
        print(f"Error in transferring data from {table_name} CSV file to the database: {e}")
        print("Error details:", e.pgcode, e.pgerror, e.diag.message_primary)

        # Rollback the transaction
        connection.rollback()


def init_db(db_name, db_password):
    tables_list = ["diseases", "has_symptoms"]

    #create_database(db_name, "postgres", db_password, "localhost", "5432")

    connection = connect(db_name, db_password)

    create_tables(connection)
    for table in tables_list:
        csv_to_db(table, connection)

    print("initialization of the database ended successfully!")

    connection.close()

# database name and password
DBname = "medhat_db"
DBpassword = "medhat123"
#init_db(DBname,DBpassword)