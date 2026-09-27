from DBCommunication import DBConnector, clean_str, setup_db_con


def get_history_item(history_id):
    con = setup_db_con()
    str_sql = (f"SELECT HistoryID, PersonID, CommandID, ResponseID, DateAchieved "
               f"FROM PersonCommandHistory WHERE HistoryID = {history_id}")

    output = con.get_dataset_query_execute(str_sql)

    if output == -1:
        return -1

    return map_person_history_data(output)


def get_all_histories():
    con = setup_db_con()
    str_sql = f"SELECT HistoryID, PersonID, CommandID, ResponseID, DateAchieved FROM PersonCommandHistory"

    output = con.get_dataset_query_execute(str_sql)

    if output == -1:
        return -1

    return map_person_history_data(output)


def get_person_history_items(person_id):
    con = setup_db_con()
    str_sql = (f"SELECT HistoryID, PersonID, CommandID, ResponseID, DateAchieved "
               f"FROM PersonCommandHistory WHERE PersonID = {person_id}")

    output = con.get_dataset_query_execute(str_sql)

    if output == -1:
        return -1

    return map_person_history_data(output)


def get_command_history_items(command_id):
    con = setup_db_con()
    str_sql = (f"SELECT HistoryID, PersonID, CommandID, ResponseID, DateAchieved "
               f"FROM PersonCommandHistory WHERE CommandID = {command_id}")

    output = con.get_dataset_query_execute(str_sql)

    if output == -1:
        return -1

    return map_person_history_data(output)


def get_response_history_items(response_id):
    con = setup_db_con()
    str_sql = (f"SELECT HistoryID, PersonID, CommandID, ResponseID, DateAchieved "
               f"FROM PersonCommandHistory WHERE ResponseID = {response_id}")

    output = con.get_dataset_query_execute(str_sql)

    if output == -1:
        return -1

    return map_person_history_data(output)


def create_history_item(person_id, command_id, response_id):
    con = setup_db_con()
    str_sql = (f"INSERT INTO PersonCommandHistory (PersonID, CommandID, ResponseID) VALUES "
               f"({person_id}, {command_id}, {response_id})")
    output = con.insert_update_query_execute(str_sql)

    if output == -1:
        return -1

    return output


def map_person_history_data(dbrows):
    return_list = []

    for row in dbrows:
        row_map = {
            "HistoryID": row[0],
            "PersonID": row[1],
            "CommandID": row[2],
            "ResponseID": row[3],
            "DateAchieved": row[4],
        }

        return_list.append(row_map)

    return return_list
