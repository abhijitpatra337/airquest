import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv


#load the bd connection params from env file
load_dotenv(".env")
def connect_to_database():
    try:
        # Cconnect to database
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER_NAME"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST_NAME"),
            port=os.getenv("PORT")
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

def close_database_connection(conn):
    try:
        if conn is not None:
            conn.close()
            print("Database connection closed.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while closing database connection:", error)

def insert_flight_details(conn, flight_id, flight_no, flight_status, aircraft_code, departure_timestamp, arrival_timestamp, departure_airport, arrival_airport):
    try:
        if conn is None:
            print("Database connection is not established.")
            return False

        # Create a cursor object using the cursor() method
        cursor = conn.cursor()

        # Define the PostgreSQL INSERT statement
        postgres_insert_query = """INSERT INTO flights (flight_id, flight_no, status, aircraft_code, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        # Execute the INSERT statement
        cursor.execute(postgres_insert_query, (flight_id, flight_no, flight_status, aircraft_code, departure_timestamp, arrival_timestamp, departure_airport, arrival_airport))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor (the connection will be closed later)
        cursor.close()

        return True  # Return True if insertion is successful

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting flight details:", error)
        return False


def insert_airport_details(conn, airport_code, airport_name, city, airport_timezone):
    try:
        if conn is None:
            print("Database connection is not established.")
            return False

        # Create a cursor object using the cursor() method
        cursor = conn.cursor()

        # Define the PostgreSQL INSERT statement
        postgres_insert_query = """INSERT INTO airports_data (airport_code, airport_name, city, timezone)
                                    VALUES (%s, %s, %s, %s)"""

        # Execute the INSERT statement
        cursor.execute(postgres_insert_query, (airport_code, airport_name, city, airport_timezone))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor (the connection will be closed later)
        cursor.close()

        return True  # Return True if insertion is successful

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting airport details:", error)
        return False


def insert_aircraft_details(conn, aircraft_code, model, range):
    try:
        if conn is None:
            print("Database connection is not established.")
            return False

        # Create a cursor object using the cursor() method
        cursor = conn.cursor()

        # Define the PostgreSQL INSERT statement
        postgres_insert_query = """INSERT INTO aircrafts_data (aircraft_code, model, range)
                                    VALUES (%s, %s, %s)"""

        # Execute the INSERT statement
        cursor.execute(postgres_insert_query, (aircraft_code, model, range))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor (the connection will be closed later)
        cursor.close()

        return True  # Return True if insertion is successful
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting airport details:", error)
        return False
    
#fetch query
def execute_query(conn, query):
    try:
        # Create a cursor
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all the results
        results = cursor.fetchall()

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Close the cursor
        cursor.close()

        return results, columns
    except psycopg2.Error as e:
        print("Error while executing query:", e)
        return None, None

def fetch_table_data(query):
    # Connect to the database
    conn = connect_to_database()
    if conn is None:
        return None

    # Execute the query
    results, columns = execute_query(conn, query)
    if results is None or columns is None:
        conn.close()
        return None

    # Close the connection
    conn.close()

    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(results, columns=columns)

    return df