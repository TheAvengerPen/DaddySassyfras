from DBCommunication import DBConnector

def setup_db_con():
    return DBConnector(usrnm="root", pswrd="Password1", dbnm="sassyfas")

def get_person_data(person_id):
    return_list = []
    con = setup_db_con()
    output = con.get_dataset_query_execute(f"SELECT PersonID, TwitchPersonName, IsStreamer FROM People WHERE PersonID = '{person_id}';")

    if output == -1:
        return -1

    for row in output:
        row_map = {
            "PersonID": row[0],
            "TwitchName": row[1],
            "IsStreamer": row[2]
        }

        return_list.append(row_map)

    return return_list
