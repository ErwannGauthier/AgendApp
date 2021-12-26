import sqlite3

from utility.dbUtil import dbConnection, dbDisconnection


def create_table(table_sql):
    function_name = "create_table"

    conn, cursor = dbConnection(function_name)

    try:
        cursor.execute(table_sql)

    except sqlite3.Error as error:
        print(f"{function_name}:\n"
              f"SQLite3 error: {error}")

    finally:
        dbDisconnection(function_name, conn, cursor)


table_server = "CREATE TABLE server (id INTEGER NOT NULL, name STRING NOT NULL, joining_date TIMESTAMP NOT NULL, leaving_date TIMESTAMP NOT NULL, id_role_admin INTEGER NOT NULL, PRIMARY KEY (id, joining_date));"
table_user = "CREATE TABLE user (id INTEGER NOT NULL, name STRING NOT NULL, PRIMARY KEY (id));"
table_server_members = "CREATE TABLE server_members (user_id INTEGER NOT NULL, server_id INTEGER NOT NULL, server_joining_date TIMESTAMP NOT NULL, PRIMARY KEY (user_id, server_id, server_joining_date), FOREIGN KEY (server_id, server_joining_date) REFERENCES server (id, joining_date) ON DELETE CASCADE, FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE);"
table_subject = "CREATE TABLE subject (id INTEGER NOT NULL, server_id INTEGER NOT NULL, server_joining_date TIMESTAMP NOT NULL, name STRING NOT NULL, diminutive STRING NOT NULL, PRIMARY KEY (id, server_id, server_joining_date), FOREIGN KEY (server_id, server_joining_date) REFERENCES server (id, joining_date) ON DELETE CASCADE);"
table_group = "CREATE TABLE [group] (id INTEGER NOT NULL, name STRING NOT NULL, server_id INTEGER NOT NULL, server_joining_date TIMESTAMP NOT NULL, PRIMARY KEY (id), FOREIGN KEY (server_id, server_joining_date) REFERENCES server (id, joining_date) ON DELETE CASCADE);"
table_membership = "CREATE TABLE membership (user_id INTEGER NOT NULL, server_id INTEGER NOT NULL, server_joining_date TIMESTAMP NOT NULL, group_id INTEGER NOT NULL, PRIMARY KEY (user_id, server_id, server_joining_date, group_id), FOREIGN KEY (server_id, server_joining_date) REFERENCES server (id, joining_date) ON DELETE CASCADE, FOREIGN KEY (group_id) REFERENCES [group] (id) ON DELETE CASCADE, FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE);"
table_homework = "CREATE TABLE homework (id INTEGER NOT NULL, server_id INTEGER NOT NULL, server_joining_date TIMESTAMP NOT NULL, subject_id INTEGER NOT NULL, group_id INTEGER NOT NULL, writer_id INTEGER NOT NULL, date TIMESTAMP NOT NULL, content STRING NOT NULL, PRIMARY KEY (id), FOREIGN KEY (server_id, server_joining_date, subject_id) REFERENCES subject (server_id, server_joining_date, id) ON DELETE CASCADE, FOREIGN KEY (group_id) REFERENCES [group] (id) ON DELETE CASCADE, FOREIGN KEY (writer_id) REFERENCES user (id) ON DELETE CASCADE);"

create_table(table_server)
create_table(table_user)
create_table(table_server_members)
create_table(table_subject)
create_table(table_group)
create_table(table_membership)
create_table(table_homework)
