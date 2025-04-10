import mysql.connector
from util.property_util import PropertyUtil

class DBConnection:
    _connection = None

    @staticmethod
    def get_connection():
        """Establishes and returns a MySQL database connection using config.ini."""
        try:
            if DBConnection._connection is None or not DBConnection._connection.is_connected():
                db_config = PropertyUtil.get_database_config()
                DBConnection._connection = mysql.connector.connect(
                    host=db_config["host"],
                    user=db_config["user"],
                    password=db_config["password"],
                    database=db_config["database"]
                )
            return DBConnection._connection
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    @staticmethod
    def close_connection():
        """Closes the database connection if it's open."""
        if DBConnection._connection and DBConnection._connection.is_connected():
            DBConnection._connection.close()
            DBConnection._connection = None
