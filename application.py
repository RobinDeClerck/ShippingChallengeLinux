import os
import web

# ONLY IN DEBUG
# from dotenv import load_dotenv
# load_dotenv()

# IMPORT ENV
DATABASE_HOST = os.getenv("DATABASE_HOST", "mysql-service")
DATABASE_DB = os.getenv("DATABASE_DB", "shippingChallenge")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "root")


def setup_database_connection():
    # CONNECTION TO SQL SERVER #
    import mysql.connector

    mydb = mysql.connector.connect(
        user=DATABASE_USER,
        passwd=DATABASE_PASSWORD,

        host=DATABASE_HOST,
        port=DATABASE_PORT,

        database=DATABASE_DB,
    )
    return mydb

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        # DB Connection
        database = setup_database_connection()
        cursor = database.cursor()

        db_query = 'SELECT surname FROM User WHERE userId = 1'
        cursor.execute(db_query)

        surname = cursor.fetchone()[0]

        return 'Hi ' + str(surname)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()