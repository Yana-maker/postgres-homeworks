import json

import psycopg2
import sqlite3 as sq

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    create_database(db_name, params)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(database_name: str, params: dict) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(database='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')


    cur.close()
    conn.close()

def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""

    cur.execute(open(script_file, "r").read())



def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    cur.execute('''CREATE TABLE if not exists suppliers(
        supplier_id serial primary key,
        company_name text NOT NULL,
        contact_name text,
        address text,
        phone text,
        fax text,
        homepage text,
        products text);'''

    )


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        to_db = [(i['company_name'], i['contact'], i['address'], i['phone'], i['fax'], i['homepage'], i['products']) for i in data]
        return to_db


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    cur.executemany('INSERT INTO suppliers(company_name, contact_name, address, phone, fax, homepage, products) VALUES (%s, %s, %s, %s, %s, %s, %s);', (suppliers))


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    pass


if __name__ == '__main__':
    main()

