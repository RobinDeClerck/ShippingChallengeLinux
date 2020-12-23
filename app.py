from flask import Flask

DATABASE_HOST="database"
DATABASE_DB="shippingChallenge"
DATABASE_PORT="3306"
DATABASE_USER="root"
DATABASE_PASSWORD="root"

app = Flask(__name__)

# ----- SQL DATABASE FUNCTIONS ----- #
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


@app.route('/')
def showUserName():
    # DB Connection
    database = setup_database_connection()
    cursor = database.cursor()

    db_query = 'SELECT surname FROM User WHERE userId = 1'
    cursor.execute(db_query)

    surname = cursor.fetchone()[0]

    return 'Hi ' + str(surname)


if __name__ == '__main__':
    app.run()
