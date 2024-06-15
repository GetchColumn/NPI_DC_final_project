import argparse
from mysql.connector import connect, Error
from config import db_login, db_password

if __name__ == '__main__':
    try:
        with connect(
            host="localhost",
            user=db_login,
            password=db_password,
            database='cinemadb_2'
        ) as connection:
            db_query = "SHOW TABLES"
            with connection.cursor() as cursor:
                cursor.execute(db_query)
                for db in cursor:
                    print(db)
            print(connection)
    except Error as e:
        print(e)