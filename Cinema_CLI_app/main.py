import argparse
import os
import time
from mysql.connector import connect, Error
from config import db_login, db_password, db_name


def show_tables(connection):
    db_query = "SHOW TABLES"
    with connection.cursor() as cursor:
        cursor.execute(db_query)
        for table in cursor:
            print(table)


def add_data(connection, table_name, data):
    # Пример: INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...)
    db_query = f"INSERT INTO {table_name} VALUES {data}"
    with connection.cursor() as cursor:
        cursor.execute(db_query)
        connection.commit()
        print("Данные успешно добавлены.")


def check_user(connection, username, password):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT role FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return user.get('role')
    else:
        return None


def display_welcome():
    message = '''   ___________   __________  ______
  / ____/  _/ | / / ____/  |/  /   |   __
 / /    / //  |/ / __/ / /|_/ / /| |__/ /_
/ /____/ // /|  / /___/ /  / / ___ /_  __/
\____/___/_/ |_/_____/_/  /_/_/  |_|/_/'''
    print("Welcome to")
    print(message)


def clear():
    if os.name == 'nt':  # Для Windows
        os.system('cls')
    else:  # Для MacOS, Linux
        os.system('clear')


# 0 - администратор
# 1 - менеджер
# 3 - клиент


def display_menu():
    print("->Доступные команды:")
    print(" 1 -- Войти")
    print(" 2 -- Зарегистрироваться")
    value = input("> ")
    return value


def display_menu_0():
    print("->Доступные команды:")
    print(" 1 -- Добавить зал")
    print(" 2 -- Добавить фильм")
    print(" 3 -- Добавить сеанс")
    print(" 4 -- Регистрация пользователя ")


def main(host, user, password, database):
    display_welcome()
    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=database
        ) as connection:
            while True:
                time.sleep(1)
                clear()
                command = display_menu()

                match command:
                    case "1":
                        username = input("->Введите имя пользователя: ")
                        passwd = input("->Введите пароль пользователя: ")
                        clear()
                        user_status = check_user(connection, username, passwd)
                        match user_status:
                            case "admin":
                                print(" admin prompt")

                            case "mgr":
                                print(" manager prompt")

                            case "client":
                                print(" client prompt")

                            case __:
                                print("Неправильное имя пользователя или пароль")


                    case __:
                        print("Неправильный ввод")

                # if command == 'show':
                #     show_tables(connection)
                # elif command == 'add':
                #     table_name = input("Введите название таблицы: ")
                #     data = input("Введите данные для добавления (в формате значений через запятую): ")
                #     add_data(connection, table_name, data)
                # else:
                #     print("Некорректная команда. Попробуйте снова.")

    except Error as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', help='Хост БД')
    parser.add_argument('--user', type=str, default=db_login, help='Имя пользователя БД')
    parser.add_argument('--password', type=str, default=db_password, help='Пароль пользователя БД>')
    parser.add_argument('--database', type=str, default=db_name, help='Название БД')
    args = parser.parse_args()

    main(args.host, args.user, args.password, args.database)
