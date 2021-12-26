import sqlite3

from utility.dbUtil import dbConnection, dbDisconnection
from utility.serverUtil import get_joining_date


def is_user_in_server_members(user, guild_id):
    function_name = "is_user_in_db"

    conn, cursor = dbConnection(function_name)

    try:
        select_query = f"SELECT * FROM 'server_members' WHERE user_id='{user.id}' AND server_id='{guild_id}'"
        cursor.execute(select_query)
        data = cursor.fetchall()

        if not data:
            is_user_in_table_user(user)
            joining_date = get_joining_date(guild_id)
            insert = "INSERT INTO 'server_members' VALUES (?, ?, ?);"
            data_tuple = (user.id, guild_id, joining_date)
            cursor.execute(insert, data_tuple)
            conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def is_user_in_table_user(user):
    function_name = "is_user_in_table_user"

    conn, cursor = dbConnection(function_name)

    try:
        select_query = f"SELECT * FROM 'user' WHERE id='{user.id}'"
        cursor.execute(select_query)
        data = cursor.fetchall()

        if not data:
            insert = "INSERT INTO 'user' VALUES (?, ?);"
            data_tuple = (user.id, user.name)
            cursor.execute(insert, data_tuple)
            conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)
