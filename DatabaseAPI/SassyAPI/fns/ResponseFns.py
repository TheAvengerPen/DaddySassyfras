from DBCommunication import DBConnector, clean_str, setup_db_con


def get_responses():
    con = setup_db_con()
    sql_str = f"SELECT ResponseID, ResponseText, CommandID, ResponseProbability FROM CommandResponse;"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_command_response_data(output)


def get_command_responses(command_id):
    con = setup_db_con()
    sql_str = f"SELECT ResponseID, ResponseText, CommandID, ResponseProbability FROM CommandResponse WHERE CommandID = {command_id};"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_command_response_data(output)


def get_response(response_id):
    con = setup_db_con()
    sql_str = f"SELECT ResponseID, ResponseText, CommandID, ResponseProbability FROM CommandResponse WHERE ResponseID = {response_id}"
    output = con.get_dataset_query_execute(sql_str)

    if output == -1:
        return -1

    return map_command_response_data(output)


def create_response(response_text, command_id, response_probs):
    con = setup_db_con()
    str_sql = (f"INSERT INTO CommandResponse (ResponseText, CommandID, ResponseProbability) "
               f"VALUES ('{clean_str(response_text)}', {command_id}, {response_probs})")
    output = con.insert_update_query_execute(str_sql)

    if output == -1:
        return -1

    return output


def update_response(response_id, response_text, command_id, response_probs):
    con = setup_db_con()
    str_sql = (f"UPDATE CommandResponse set ResponseText = '{clean_str(response_text)}', "
               f"CommandID = {command_id}, ResponseProbability = {response_probs} WHERE ResponseID = {response_id}")
    output = con.insert_update_query_execute(str_sql)

    if output == -1:
        return -1

    return response_id


def delete_response(response_id):
    con = setup_db_con()
    str_sql = f"DELETE FROM CommandResponse WHERE ResponseID = {response_id}"
    output = con.delete_query_execute(str_sql)

    if output == -1:
        return -1

    return output


def map_command_response_data(dbrows):
    return_list = []

    for row in dbrows:
        row_map = {
            "ResponseID": row[0],
            "ResponseText": row[1],
            "CommandID": row[2],
            "ResponseProbability": row[3],
        }

        return_list.append(row_map)

    return return_list
