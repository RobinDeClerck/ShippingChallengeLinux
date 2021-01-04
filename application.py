import os
import web

# ONLY IN DEBUG
# from dotenv import load_dotenv
# load_dotenv()

# IMPORT ENV
DATABASE_HOST = os.getenv("DATABASE_HOST", "mysql-service")
DATABASE_DB = os.getenv("DATABASE_DB", "ShippingChallenge")
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
        try:
            # DB Connection
            database = setup_database_connection()
            cursor = database.cursor()

            db_query = 'SELECT surname FROM ShippingChallenge.User WHERE userId = 1'
            cursor.execute(db_query)

            surname = cursor.fetchone()[0]

            web.header("Content-Type", "text/html")
            bootstrap = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet">'
            google_font = '<link rel="preconnect" href="https://fonts.gstatic.com"><link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@700&display=swap" rel="stylesheet">'

            layout = \
                '<div class="container">' \
                    '<div class="row">' \
                        '<p class="text-center mt-5 display-4" style="font-family:Open Sans, sans-serif;">Hi ' + str(surname) + '</p>' \
                        '<div class="text-center">' \
                            '<img src="https://cdn.discordapp.com/attachments/668890794882629662/795444478797545492/linux.jpg" alt="Linux Joke">' \
                        '</div>' \
                    '</div>' \
                '</div>'

            return bootstrap + google_font + layout
        except Exception as error:
            return "Error: " + str(error)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()