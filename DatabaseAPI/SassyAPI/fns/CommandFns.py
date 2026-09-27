from DBCommunication import DBConnector, clean_str, setup_db_con


def get_command(command_id):
    con = setup_db_con()
    sql_str = f"SELECT CommandID, CommandName, CommandTypeID, CommandDescription, ProbabilityActivate From Command WHERE CommandID = {command_id};"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_command_data(output)


def create_new_command(command_name, command_type_id, command_description, probability_activate):
    con = setup_db_con()
    c = setup_db_con()

    sql_str = (f"INSERT INTO Command (CommandName, CommandTypeID, CommandDescription, ProbabilityActivate) "
               f"VALUES ('{clean_str(command_name)}', '{clean_str(command_type_id)}', "
               f"'{clean_str(command_description)}', {probability_activate});")
    output = con.insert_update_query_execute(sql_str)

    if output == -1:
        return -1

    return output


def update_command_info(command_id, command_name, command_type_id, command_description, probability_activate):
    con = setup_db_con()

    sql_str = (f"UPDATE Command SET CommandName = '{command_name}', CommandTypeID='{command_type_id}', "
               f"CommandDescription='{command_description}', ProbabilityActivate={probability_activate} WHERE CommandID = {command_id};")
    output = con.insert_update_query_execute(sql_str)

    if output == -1:
        return -1

    return output


def get_all_commands():
    con = setup_db_con()
    sql_str = f"SELECT CommandID, CommandName, CommandTypeID, CommandDescription, ProbabilityActivate From Command;"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_command_data(output)


def delete_command(command_id):
    con = setup_db_con()
    sql_str = (f"DELETE FROM Command WHERE CommandID = {command_id};"
               f"DELETE FROM CommandPerson WHERE CommandID = {command_id};"
               f"DELETE FROM CommandResponse WHERE CommandID = {command_id};")
    output = con.delete_query_execute(sql_str)

    return output


def get_user_commands(user_id):
    con = setup_db_con()
    sql_str = (f"SELECT C.CommandID, C.CommandName, C.CommandTypeID, C.CommandDescription, C.ProbabilityActivate, CP.Active "
               f"FROM Command C RIGHT JOIN CommandPerson CP ON CP.CommandID = C.CommandID WHERE PersonID = {user_id};")
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_command_data(output, has_active=True)


def unlink_user_command(user_id, command_id):
    con = setup_db_con()
    sql_str = f"DELETE FROM CommandPerson WHERE PersonID = '{user_id}' AND CommandID = '{command_id};'"
    output = con.delete_query_execute(sql_str)

    if output == -1:
        return -1

    return output


def link_user_command(user_id, command_id):
    con = setup_db_con()
    sql_str = f"SELECT COUNT(*) FROM CommandPerson WHERE PersonID = {user_id} AND CommandID = {command_id};"
    output = con.get_dataset_query_execute(sql_str)

    if output[0][0] > 0:
        return -2

    sql_str = f"INSERT INTO CommandPerson (PersonID, CommandID) VALUES ({user_id}, {command_id});"
    output = con.insert_update_query_execute(sql_str)

    return output


def map_command_data(dbrows, has_active=False):
    return_list = []

    for row in dbrows:
        if has_active:
            row_map = {
                "CommandID": row[0],
                "CommandName": row[1],
                "CommandTypeID": row[2],
                "CommandDescription": row[3],
                "ProbabilityActivate": row[4],
                "Active": row[5],
            }
        else:
            row_map = {
                "CommandID": row[0],
                "CommandName": row[1],
                "CommandTypeID": row[2],
                "CommandDescription": row[3],
                "ProbabilityActivate": row[4],
            }

        return_list.append(row_map)

    return return_list
