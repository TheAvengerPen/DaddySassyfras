from DBCommunication import DBConnector, clean_str, setup_db_con


def get_person_data(person_id):
    con = setup_db_con()
    sql_str = f"SELECT PersonID, TwitchPersonName, IsStreamer FROM People WHERE PersonID = '{person_id}';"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_person_data(output)


def get_person_data_twitch_id(twitch_name):
    con = setup_db_con()
    sql_str = f"SELECT PersonID, TwitchPersonName, IsStreamer FROM People WHERE TwitchPersonName = '{twitch_name}';"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_person_data(output)


def create_new_user(twitch_name, is_streamer):
    con = setup_db_con()
    if not is_streamer or is_streamer == 0 or is_streamer == "false":
        is_streamer = 0
    else:
        is_streamer = 1

    sql_str = f"INSERT INTO People (TwitchPersonName, IsStreamer) VALUES ('{clean_str()}', {is_streamer});"
    output = con.insert_update_query_execute(sql_str)

    if output == -1:
        return -1

    return output


def update_user_info(person_id, twitch_name, is_streamer):
    con = setup_db_con()
    if not is_streamer or is_streamer == 0 or is_streamer == "false":
        is_streamer = 0
    else:
        is_streamer = 1

    sql_str = f"UPDATE People SET TwitchPersonName = '{twitch_name}', IsStreamer={is_streamer} WHERE PersonID = {person_id};"
    output = con.insert_update_query_execute(sql_str)

    if output == -1:
        return -1

    return output


def get_all_users():
    con = setup_db_con()
    sql_str = f"SELECT PersonID, TwitchPersonName, IsStreamer FROM People;"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_person_data(output)


def delete_user(user_id):
    con = setup_db_con()
    sql_str = (f"DELETE FROM People WHERE PersonID = {user_id};"
               f"DELETE FROM CommandPerson WHERE PersonID = {user_id};"
               f"DELETE FROM PersonCommandHistory WHERE PersonID = {user_id}")
    output = con.delete_query_execute(sql_str)

    return output


def get_users_from_command(command_id):
    con = setup_db_con()
    sql_str = f"SELECT P.PersonID, P.TwitchPersonName, P.IsStreamer FROM People P RIGHT JOIN CommandPerson CP ON P.PersonID = CP.PersonID WHERE CommandID = {command_id};"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_person_data(output)


def map_person_data(dbrows):
    return_list = []

    for row in dbrows:
        row_map = {
            "PersonID": row[0],
            "TwitchName": row[1],
            "IsStreamer": row[2]
        }

        return_list.append(row_map)

    return return_list
