import sqlite3

from utility.dbUtil import dbConnection, dbDisconnection
from utility.functionUtil import init_group_role
from utility.membershipUtil import add_membership_in_db
from utility.serverUtil import get_joining_date
from utility.userUtil import is_user_in_server_members


async def add_group_in_db(guild, group_name):
    function_name = "add_group_in_db"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild.id)

    try:
        group_id = await init_group_role(guild, group_name)
        insert = "INSERT INTO 'group' VALUES (?, ?, ?, ?);"
        data_tuple = (group_id, group_name, guild.id, j_date)
        cursor.execute(insert, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def add_group_to_user_having_role(role):
    for member in role.members:
        is_user_in_server_members(member, role.guild.id)
        add_membership_in_db(member.id, role.guild.id, role.id)


def add_role_in_db(guild_id, group_id, group_name):
    function_name = "add_role_in_db"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        insert = "INSERT INTO 'group' VALUES (?, ?, ?, ?);"
        data_tuple = (group_id, group_name, guild_id, j_date)
        cursor.execute(insert, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def delete_group(group_id):
    function_name = "delete_group"

    conn, cursor = dbConnection(function_name)

    try:
        delete = f"DELETE FROM 'group' WHERE id = {group_id}"
        cursor.execute(delete)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def get_groups_list(guild_id):
    function_name = "get_groups_list"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        select_query = f"SELECT name FROM 'group' WHERE server_id='{guild_id}' AND server_joining_date='{j_date}'"
        cursor.execute(select_query)
        data = cursor.fetchall()

        return list(data)

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def is_group_id_in_table_group(guild_id, group_id):
    function_name = "is_group_name_in_table_group"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        result = True
        select_query = f"SELECT * FROM 'group' WHERE server_id='{guild_id}' AND server_joining_date='{j_date}' AND id='{group_id}'"
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


def is_group_name_in_table_group(guild_id, group_name):
    function_name = "is_group_name_in_table_group"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        result = True
        select_query = f"SELECT * FROM 'group' WHERE server_id='{guild_id}' AND server_joining_date='{j_date}' AND name='{group_name}'"
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


def update_group_name(group_id, group_name):
    function_name = "update_group_name"

    conn, cursor = dbConnection(function_name)

    try:
        update = f"UPDATE 'group' SET name = ? WHERE id = ?"
        data_tuple = (group_name, group_id)
        cursor.execute(update, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)
