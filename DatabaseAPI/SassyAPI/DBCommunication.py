import pyodbc


class SassSQLCall:
    connection = None

    def __init__(self, dbServerName, dbName):
        connectionString = ("Driver={ODBC Driver 18 for SQL Server};" + "Server=" + dbServerName + ";" + "Database=" + dbName + ";" +
                            "Trusted_Connection=yes;" + "UID=ApenguinsLullaby;PWD=")
        print(connectionString)
        self.connection = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};"
                                         "Server=APenguinsLullab;"
                                         "Database=DaddySassyfras;"
                                         "Trusted_Connection=yes;"
                                         "UID=ApenguinsLullaby;PWD=")

    def execute(self, sqlString):
        returnList = []

        cursor = self.connection.cursor()
        cursor.execute(sqlString)

        for row in cursor:
            print(row)
