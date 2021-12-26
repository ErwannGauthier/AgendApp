import sqlite3
from datetime import datetime

from utility.dbUtil import dbConnection, dbDisconnection
from utility.serverUtil import get_admin_role_id, get_joining_date


async def add_role_to_user(user, role):
    await user.add_roles(role)


def add_year_to_date(date):

    if len(date) == 5:
        date = date + f"/{datetime.now().year}"
    elif len(date) == 8:
        date_time_obj = datetime.strptime(date, '%m/%d/%y')
        date = date[:6] + f"{date_time_obj.year}"

    return date


def add_year_to_french_date(date):
    if len(date) == 5:
        date = date + f"/{datetime.now().year}"
    elif len(date) == 8:
        date_time_obj = datetime.strptime(date, '%d/%m/%y')
        date = date[:6] + f"{date_time_obj.year}"

    return date


def arg_into_list(args):
    liste = []
    for i in range(len(args)):
        liste.append(args[i].capitalize())

    return liste


def convert_date_into_str(date):
    return f"{date.month}/{date.day}/{date.year}"


def convert_french_date_into_str(date):
    return f"{date.day}/{date.month}/{date.year}"


def convert_str_into_date(date):
    return datetime.strptime(date, '%m/%d/%Y')


def convert_str_into_french_date(date):
    return datetime.strptime(date, '%d/%m/%Y')


async def delete_role(ctx, role_id):
    role = ctx.guild.get_role(role_id)

    await role.delete()


def get_date(elem):
    return elem[4]


async def have_admin_role(ctx):
    role_id = get_admin_role_id(ctx.guild.id)
    result = ctx.guild.get_role(role_id) in ctx.author.roles
    if not result:
        await ctx.send(">>> Vous n'avez pas la permission d'exécuter cette commande.")

    return result


async def init_agendadmin_role(guild):
    role_name = "Agend'Admin"
    agendadmin = await guild.create_role(name=role_name, mentionable="True", colour=int("ccdf35", 16))

    for member in guild.members:
        if member.guild_permissions.administrator:
            await member.add_roles(agendadmin)

    return agendadmin.id


async def init_group_role(guild, role_name):
    role = await guild.create_role(name=role_name, mentionable="True", colour=int("ccdf35", 16))

    return role.id


def is_date_conform(date):

    res = True
    len_date = len(date)

    if len_date == 10:
        try:
            date_time_obj = datetime.strptime(date, '%m/%d/%Y')
        except:
            res = False
    elif len_date == 8:
        try:
            date_time_obj = datetime.strptime(date, '%m/%d/%y')
        except:
            res = False
    elif len_date == 5:
        try:
            date_time_obj = datetime.strptime(date, '%m/%d')
        except:
            res = False
    else:
        res = False

    return res


def is_date_not_passed(date):
    len_date = len(date)
    now = datetime.now()

    if is_date_conform(date):
        if len_date == 10:
            date_time_obj = datetime.strptime(date, '%m/%d/%Y')
        elif len_date == 8:
            date_time_obj = datetime.strptime(date, '%m/%d/%y')
        elif len_date == 5:
            date_time_obj = datetime.strptime(date, '%m/%d')

    try:
        if date_time_obj.year == 1900:
            date_time_obj = date_time_obj.replace(year=now.year)

        delta = now - date_time_obj
    except:
        return False

    return delta.days <= 0


def is_french_date_conform(date):

    res = True
    len_date = len(date)

    if len_date == 10:
        try:
            date_time_obj = datetime.strptime(date, '%d/%m/%Y')
        except:
            res = False
    elif len_date == 8:
        try:
            date_time_obj = datetime.strptime(date, '%d/%m/%y')
        except:
            res = False
    elif len_date == 5:
        try:
            date_time_obj = datetime.strptime(date, '%d/%m')
        except:
            res = False
    else:
        res = False

    return res


def is_french_date_not_passed(date):
    len_date = len(date)
    now = datetime.now()

    if is_french_date_conform(date):
        now = datetime.strptime(f"{now.day}/{now.month}/{now.year}", "%d/%m/%Y")
        if len_date == 10:
            date_time_obj = datetime.strptime(date, '%d/%m/%Y')
            strtoday = "%d/%m/%Y"
        elif len_date == 8:
            date_time_obj = datetime.strptime(date, '%d/%m/%y')
            strtoday = "%d/%m/%y"
        elif len_date == 5:
            date_time_obj = datetime.strptime(date, '%d/%m')
            strtoday = "%d/%m"

    try:
        if date_time_obj.year == 1900:
            date_time_obj = date_time_obj.replace(year=now.year)

        delta = now - date_time_obj
    except:
        return False

    return delta.days <= 0


async def remove_role(user, role):
    await user.remove_roles(role)


async def verif_agendadmin_exist(role):
    function_name = "verif_agendadmin_exist"

    conn, cursor = dbConnection(function_name)

    try:
        select_query = f"SELECT id_role_admin FROM 'server' WHERE id = '{role.guild.id}' AND joining_date = leaving_date"
        cursor.execute(select_query)
        data = cursor.fetchall()

        for row in data:
            if row[0] == role.id:
                role_admin = await init_agendadmin_role(role.guild)

                update = f"UPDATE server SET id_role_admin = ? WHERE id = ? AND joining_date = leaving_date"
                data_tuple = (role_admin, role.guild.id)
                cursor.execute(update, data_tuple)
                conn.commit()

    except sqlite3.Error or ValueError as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


def verif_dont_starts_and_ends_with_space(grp):
    group = grp

    while group.startswith(" "):
        group = group[1:]

    while group.endswith(" "):
        group = group[:-1]

    return group


def verif_not_group_role(role):
    function_name = "verif_not_group_role"

    conn, cursor = dbConnection(function_name)

    j_date = get_joining_date(role.guild.id)

    try:
        select_query = f"SELECT id FROM 'group' WHERE server_id = '{role.guild.id}' AND server_joining_date = '{j_date}'"
        cursor.execute(select_query)
        data = cursor.fetchall()

        for row in data:
            if row[0] == role.id:
                delete = f"DELETE FROM 'group' WHERE id = {role.id}"
                cursor.execute(delete)
                conn.commit()

    except sqlite3.Error or ValueError as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)