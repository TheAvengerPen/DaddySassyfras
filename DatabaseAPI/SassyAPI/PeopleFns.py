from DBCommunication import DBConnector


def setup_db_con():
    return DBConnector(usrnm="root", pswrd="Password1", dbnm="sassyfas")


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

    sql_str = f"INSERT INTO People (TwitchPersonName, IsStreamer) VALUES ('{twitch_name}', {is_streamer});"
    print(sql_str)
    output = con.insert_update_query_execute(sql_str)

    print(output)

    if output == -1:
        return -1

    return output

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
