import sqlite3


def dbConnection(function_name):
    try:
        conn = sqlite3.connect('AgendApp_DB.db')
        # print(f"{function_name} is connected to data base.")
        return conn, conn.cursor()

    except sqlite3.Error as error:
        print(f"{function_name} in dbConnection:\n"
              f"SQLite3 error: {error}")


def dbDisconnection(function_name, conn, cursor):
    try:
        cursor.close()
        conn.close()
        # print(f"{function_name} is disconnected from data base.")

    except sqlite3.Error as error:
        print(f"{function_name} in dbDisconnection:\n"
              f"SQLite3 error: {error}")
