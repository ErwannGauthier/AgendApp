import datetime
import sqlite3

from utility.dbUtil import dbDisconnection, dbConnection


def add_server(guild, role_admin):
    function_name = "add_server"

    conn, cursor = dbConnection(function_name)

    try:
        date = datetime.datetime.now()

        insert = "INSERT INTO server VALUES (?, ?, ?, ?, ?);"
        data_tuple = (guild.id, guild.name, date, date, role_admin)

        cursor.execute(insert, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def delete_server(guild_id):
    function_name = "delete_server"

    conn, cursor = dbConnection(function_name)
    date = datetime.datetime.now()

    try:
        update = f"UPDATE server SET leaving_date = ? WHERE id = ? AND joining_date = leaving_date"
        data_tuple = (date, guild_id)
        cursor.execute(update, data_tuple)
        conn.commit()

        tables = ["homework", "membership", "server_members", "group", "subject"]
        for table in tables:
            try:
                request = f"DELETE FROM '{table}' WHERE server_id = '{guild_id}'"
                cursor.execute(request)
                conn.commit()

            except sqlite3.Error as error:
                print(f"{function_name}: \n"
                      f"SQLite3 error: {error}")

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def get_admin_role_id(guild_id):
    function_name = "get_admin_role_id"

    conn, cursor = dbConnection(function_name)
    try:
        j_date = get_joining_date(guild_id)
        select_query = f"SELECT id_role_admin FROM 'server' WHERE id='{guild_id}' AND joining_date='{j_date}' AND joining_date = leaving_date"
        cursor.execute(select_query)
        data = cursor.fetchall()

        for row in data:
            return row[0]

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def get_joining_date(guild_id):
    function_name = "get_joining_date"

    conn, cursor = dbConnection(function_name)
    try:
        select_query = f"SELECT joining_date FROM 'server' WHERE id='{guild_id}' AND joining_date = leaving_date"
        cursor.execute(select_query)
        data = cursor.fetchall()

        for row in data:
            return row[0]

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)
