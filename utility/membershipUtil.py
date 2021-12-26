import sqlite3

from utility.dbUtil import dbConnection, dbDisconnection
from utility.serverUtil import get_joining_date


def add_membership_in_db(user_id, server_id, group_id):
    function_name = "add_membership_in_db"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(server_id)

    try:
        insert = "INSERT INTO 'membership' VALUES (?, ?, ?, ?);"
        data_tuple = (user_id, server_id, j_date, group_id)
        cursor.execute(insert, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def delete_membership(user_id, server_id, group_id):
    function_name = "delete_membership"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(server_id)

    try:
        delete = "DELETE FROM 'membership' WHERE user_id = ? AND server_id = ? AND server_joining_date = ? AND group_id = ?;"
        data_tuple = (user_id, server_id, j_date, group_id)
        cursor.execute(delete, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def is_membership_set(server_id, user_id, group_id):
    function_name = "is_membership_set"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(server_id)

    try:
        res = True

        select = "SELECT * FROM 'membership' WHERE user_id = ? AND server_id = ? AND server_joining_date = ? AND group_id = ?;"
        data_tuple = (user_id, server_id, j_date, group_id)
        cursor.execute(select, data_tuple)
        data = cursor.fetchall()

        if not data:
            res = False

        return res

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def is_user_in_membership_table(server_id, user_id):
    function_name = "is_user_in_membership_table"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(server_id)

    try:
        res = True

        select = "SELECT * FROM 'membership' WHERE user_id = ? AND server_id = ? AND server_joining_date = ?"
        data_tuple = (user_id, server_id, j_date)
        cursor.execute(select, data_tuple)
        data = cursor.fetchall()

        if not data:
            res = False

        return res

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)
