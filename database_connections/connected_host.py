import pyodbc
from database_connections import azure_configuration


def get_connected_host():
    server = azure_configuration.sql_server
    database = azure_configuration.sql_database
    username = azure_configuration.sql_db_username
    password = azure_configuration.sql_db_password
    driver = '{ODBC Driver 18 for SQL Server}'
    l = []
    print('CONNECTED HOST:')
    with pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM HOST")
            row = cursor.fetchone()
            while row:
                print("\t" + str(row[0]) + " - " + str(row[1]))
                l.append(row[1])
                row = cursor.fetchone()
    return l