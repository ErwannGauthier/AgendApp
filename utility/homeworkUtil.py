import sqlite3
from datetime import datetime

from utility.dbUtil import dbConnection, dbDisconnection
from utility.functionUtil import convert_str_into_french_date, get_date, convert_french_date_into_str
from utility.serverUtil import get_joining_date


def add_homework_in_db(guild_id, subject_id, group_id, writer_id, date, content):
    function_name = "add_homework_in_db"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        id = calc_homework_id()
        insert = "INSERT INTO 'homework' VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        data_tuple = (id, guild_id, j_date, subject_id, group_id, writer_id, date, content)
        cursor.execute(insert, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def calc_homework_id():
    function_name = "calc_homework_id"

    conn, cursor = dbConnection(function_name)

    try:
        id = 0

        select_query = "SELECT MAX(id) FROM 'homework'"
        cursor.execute(select_query)
        data = cursor.fetchall()

        for row in data:
            if row[0] is not None:
                id = row[0] + 1

        return id

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def delete_homework(guild_id, subject_id, group_id, id_author, date, content):
    function_name = "delete_homework"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        delete = "DELETE FROM homework WHERE server_id = ? AND server_joining_date = ? AND subject_id = ? AND group_id = ? AND writer_id = ? AND date = ? AND content = ?"
        data_tuple = (guild_id, j_date, subject_id, group_id, id_author, date, content)
        cursor.execute(delete, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def is_homework_already_in_db(guild_id, subject_id, group_id, date):
    function_name = "is_homework_already_in_db"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        res = False
        homework = ""
        select = "SELECT s.name, h.date, u.name, h.writer_id, h.content FROM homework h LEFT JOIN subject s ON h.subject_id = s.id AND h.server_id = s.server_id AND h.server_joining_date = s.server_joining_date LEFT JOIN user u ON h.writer_id = u.id WHERE h.server_id = ? AND h.server_joining_date = ? AND h.subject_id = ? AND h.group_id = ? AND h.date = ?"
        data_tuple = (guild_id, j_date, subject_id, group_id, date)
        cursor.execute(select, data_tuple)
        data = cursor.fetchall()

        if data:
            res = True
            for row in data:
                homework = homework + f"Matière:\t`{row[0]}`\nDate:\t\t  `{row[1]}`\nÉcrit par:\t`{row[2]} #{row[3]}`\nContenu:\t`{row[4]}`\n\n"

        return res, homework

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def is_homework_in_db(guild_id, subject_id, group_id, id_author, date, content):
    function_name = "is_homework_in_db"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(guild_id)

    try:
        res = False
        homework = ""
        select = "SELECT s.name, h.date, u.name, h.writer_id, h.content FROM homework h LEFT JOIN subject s ON h.subject_id = s.id AND h.server_id = s.server_id AND h.server_joining_date = s.server_joining_date LEFT JOIN user u ON h.writer_id = u.id WHERE h.server_id = ? AND h.server_joining_date = ? AND h.subject_id = ? AND h.group_id = ? AND h.writer_id = ? AND h.date = ? AND h.content = ?"
        data_tuple = (guild_id, j_date, subject_id, group_id, id_author, date, content)
        cursor.execute(select, data_tuple)
        data = cursor.fetchall()

        if data:
            res = True
            for row in data:
                homework = homework + f"Matière:\t`{row[0]}`\nDate:\t\t  `{row[1]}`\nÉcrit par:\t`{row[2]} #{row[3]}`\nContenu:\t`{row[4]}`\n\n"

        return res, homework

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def list_homeworks(server_id, user_id):
    function_name = "list_homeworks"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(server_id)

    try:
        select = "SELECT s.name, g.name, u.id, u.name, h.date, h.content FROM homework h LEFT JOIN subject s ON h.subject_id = s.id AND h.server_id = s.server_id AND h.server_joining_date = s.server_joining_date LEFT JOIN 'group' g ON h.group_id = g.id AND h.server_id = g.server_id AND h.server_joining_date = g.server_joining_date LEFT JOIN user u ON h.writer_id = u.id LEFT JOIN membership m ON h.group_id = m.group_id AND h.server_id = m.server_id AND h.server_joining_date = m.server_joining_date WHERE h.server_id = ? AND h.server_joining_date = ? AND m.user_id = ? ORDER BY h.group_id ASC;"
        data_tuple = (server_id, j_date, user_id)
        cursor.execute(select, data_tuple)
        datas = cursor.fetchall()

        data = [list(i) for i in datas]
        if not datas:
            res = ">>> Vous n'avez pas de devoir."
        else:
            group = []
            remove = []
            for row in data:
                row[4] = convert_str_into_french_date(row[4])
                delta = (row[4] - datetime.now()).days
                if delta < 0:
                    remove.append(row)

            for rows in remove:
                data.remove(rows)

            if len(data) > 0:
                res = f">>> Vous avez {len(data)} devoirs:"
                for row in data:
                    if row[1] not in group:
                        group.append(row[1])
                        current = []
                        for row2 in data[data.index(row):]:
                            if row[1] == row2[1]:
                                current.append(row2)

                        current.sort(key=get_date)

                        res = res + f"\n\n**Groupe `{row[1]}`:**"

                        current_date = current[0][4]
                        delta = (current_date - datetime.now()).days
                        if delta >= 0:
                            res = res + f"\n\tPour le `{convert_french_date_into_str(current_date)}`"

                        for homework in current:
                            if homework[4] != current_date:
                                current_date = homework[4]
                                delta = (current_date - datetime.now()).days
                                if delta >= 0:
                                    res = res + f"\n\tPour le `{convert_french_date_into_str(current_date)}`"

                            if delta >= 0:
                                res = res + f"\n\n\t\tMatière: `{homework[0]}`\n\t\tContenu: `{homework[5]}`\n\t\t*Ajouté par: `{homework[3]} #{homework[2]}`*\n"
            else:
                res = ">>> Vous n'avez pas de devoir."
        return res

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)
