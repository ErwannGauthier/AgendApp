import sqlite3

from utility.dbUtil import dbConnection, dbDisconnection
from utility.serverUtil import get_joining_date


def add_subject_in_db(guild_id, arg):
    function_name = "add_subject_in_db"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        subject_id = calc_subject_id(guild_id, j_date)
        insert = "INSERT INTO 'subject' VALUES (?, ?, ?, ?, ?);"
        data_tuple = (subject_id, guild_id, j_date, arg[0], arg[1])
        cursor.execute(insert, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def calc_subject_id(guild_id, j_date):
    function_name = "calc_subject_id"

    conn, cursor = dbConnection(function_name)

    try:
        subject_id = 0

        select_query = f"SELECT MAX(id) FROM 'subject' WHERE server_id='{guild_id}' AND server_joining_date='{j_date}'"
        cursor.execute(select_query)
        data = cursor.fetchall()

        for row in data:
            if row[0] is not None:
                subject_id = row[0] + 1

        return subject_id

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def delete_subject(guild_id, subj):
    function_name = "delete_subject"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        delete = f"DELETE FROM subject WHERE server_id = {guild_id} AND server_joining_date = '{j_date}' AND (name='{subj}' OR diminutive='{subj}')"
        cursor.execute(delete)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def get_subject_id(guild_id, subj):
    function_name = "get_subject_id"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        subject_id = -1

        select_query = f"SELECT id FROM 'subject' WHERE server_id='{guild_id}' AND server_joining_date='{j_date}' AND (name='{subj}' OR diminutive='{subj}')"
        cursor.execute(select_query)
        data = cursor.fetchall()

        for row in data:
            if row[0] is not None:
                subject_id = row[0]

        return subject_id

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def get_subjects_list(guild_id):
    function_name = "get_subjects_list"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        select_query = f"SELECT name, diminutive FROM 'subject' WHERE server_id='{guild_id}' AND server_joining_date='{j_date}'"
        cursor.execute(select_query)
        data = cursor.fetchall()

        return list(data)

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def is_subject_in_table_subject(guild_id, arg):
    function_name = "is_subject_in_table_subject"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        result = True
        select_query = f"SELECT * FROM 'subject' WHERE server_id='{guild_id}' AND server_joining_date='{j_date}' AND (name='{arg[0]}' OR diminutive='{arg[1]}')"
        cursor.execute(select_query)
        data = cursor.fetchall()

        if not data:
            result = False

        return result

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)
