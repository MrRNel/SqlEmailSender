#Function to excute a query and return the results if any.
#Not equiped to deal with error logging or non returns

# sql_operations.py
import pyodbc
import pandas as pd
from config import server, database, username, password

def execute_sql_query(query):
    # Establish a connection to SQL Server
    connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)

    # Execute the SQL query and retrieve data into a Pandas DataFrame
    df = pd.read_sql(query, conn)

    # Close the database connection
    conn.close()

    return df
