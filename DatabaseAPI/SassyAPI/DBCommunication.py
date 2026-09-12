import mysql.connector

import ErrorLogging


class DBConnector:
    user_name = ""
    password = ""
    dataServer = None
    database_name = ""

    def __init__(self, usrnm, pswrd, dbnm):
        self.user_name = usrnm
        self.password = pswrd
        self.database_name = dbnm

        try:
            self.connect()
        except:
            ErrorLogging.log_error("Unable to connect to db server")

    def connect(self):
        db = mysql.connector.connect(
            host="localhost",
            user=self.user_name,
            password=self.password,
            database=self.database_name
        )

        self.dataServer = db

    def get_dataset_query_execute(self, query):
        try:
            cursor = self.dataServer.cursor()
            cursor.execute(query)

            return cursor.fetchall()
        except:
            ErrorLogging.log_error("Failed to execute SQL: " + query)
            return -1

    def insert_update_query_execute(self, query):
        try:
            cursor = self.dataServer.cursor()
            cursor.execute(query)

            return cursor.lastrowid
        except:
            ErrorLogging.log_error("Failed to execute SQL: " + query)
            return -1
