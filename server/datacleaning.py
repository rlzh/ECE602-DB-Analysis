

import pymysql
import shared
import traceback
import os
import progressbar as pbar


class DataCleaner():
    def __init__(self, host, username, password, db):
        self.host = host
        self.username = username
        self.password = password
        self.db = db

        # sql files
        sql_dir = os.path.join(shared.abs_path, "sql/")
        self.add_primary_file = os.path.join(sql_dir,"add_primary.sql")
        self.add_foreign_file = os.path.join(sql_dir,"add_foreign.sql")
        self.mismatch_file = os.path.join(sql_dir, "mismatch.sql")
        self.drop_primary_file = os.path.join(sql_dir, "drop_primary.sql")
        self.drop_foreign_file = os.path.join(sql_dir, "drop_foreign.sql")
        self.create_view_file = os.path.join(sql_dir, "createview.sql")
        self.drop_view_file = os.path.join(sql_dir,"dropview.sql")
        self.unclean_file = os.path.join(sql_dir,"unclean.sql")
        self.load_db_file = os.path.join(sql_dir,"lahman2016.sql")

    def open_connection(self):
        try:
            print("connecting to db..")
            return pymysql.connect(self.host, self.username, self.password, self.db)
        except Exception as e:
            traceback.print_exc()
            return None
    
    def close_connection(self, db_conn):
        if db_conn == None:
            return
        try:
            print("closing connection to db...")
            db_conn.close()
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    def parse_sql_file(self, file_name):
        try:
            sql_commands = []
            curr_command = ""
            f = open(file_name)
            for line in f.readlines():
                line = line.strip()
                if line.startswith("--"):
                    continue
                curr_command += line + " "
                if line.endswith(';'):
                    sql_commands.append(curr_command)
                    curr_command = ""
            return sql_commands
        except Exception as e:
            traceback.print_exc()
            return []

    def _execute_update_sql(self, file_name):
        result = True
        conn = self.open_connection()
        if conn == None:
            return False
        # parse commands from file
        sql_commands = self.parse_sql_file(file_name)
        print("executing sql from {}, # commands = {}".format(file_name, len(sql_commands)))
        # ok_error_cods = [
        #     1044,
        # ]
        with conn.cursor() as cursor:
            for i in pbar.progressbar(range(len(sql_commands))):
                sql = sql_commands[i]
                # print(sql)
                try:
                    cursor.execute(sql)
                except Exception as e:
                    print(e)
                    result = False
                    break
                    # traceback.print_exc()
        if result:
            conn.commit()
        self.close_connection(conn)
        return result

    def load_db(self):
        return self._execute_update_sql(self.load_db_file)

    def add_primary(self):
        shared.added_primary =self._execute_update_sql(self.add_primary_file)
        return shared.added_primary

    def add_foreign(self):
        shared.added_foreign = self._execute_update_sql(self.add_foreign_file)
        return shared.added_foreign

    def fix_mismatch(self):
        return self._execute_update_sql(self.mismatch_file)

    def add_all(self):
        return self.add_primary() and self.fix_mismatch() and self.add_foreign()

    def create_view(self):
        return self._execute_update_sql(self.create_view_file)
    

    def unclean(self):
        if shared.added_primary:
            shared.added_primary = not self._execute_update_sql(self.drop_primary_file)
        if shared.added_foreign:
            shared.added_foreign = not self._execute_update_sql(self.drop_foreign_file)
        return shared.added_primary == False \
            and shared.added_foreign == False \
            and self._execute_update_sql(self.unclean_file) \
            and self._execute_update_sql(self.drop_view_file)


def handle_clean(msg_data):
    return True
    accepted = [
        "Add Primary Only",
        "Add Primary and Foreign",
        "Mismatching Values",
        "All",
    ]
    if len(msg_data) > 1:
        print("Error: Too many options {}".format(msg_data))
        return False
    option = msg_data[0]
    if option not in accepted:
        print("Error: Invalid option {}".format(option))
        return False

    cleaner = DataCleaner(
        shared.host,
        shared.user,
        shared.password,
        shared.database
    )

    if option == accepted[0]:
        return cleaner.add_primary() and cleaner.create_view()
    elif option == accepted[1]:
        return cleaner.add_primary() \
            and cleaner.fix_mismatch() \
                and cleaner.add_foreign() \
                    and cleaner.create_view()
    elif option == accepted[2]:
        return cleaner.add_primary() \
            and cleaner.fix_mismatch() \
            and cleaner.create_view()
    elif option == accepted[3]:
        return cleaner.add_all() \
            and cleaner.create_view() 
    return False

def handle_unclean():
    cleaner = DataCleaner(
        shared.host,
        shared.user,
        shared.password,
        shared.database
    )
    return cleaner.unclean()

