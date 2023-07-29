import psycopg2
import csv

def read_csv_customers_file():
    with open ('../homework-1/north_data/customers_data.csv', 'r', encoding='utf-8') as file:
        data = csv.DictReader(file)
        to_db = [(i['customer_id'], i['company_name'], i['contact_name']) for i in data]
        return to_db

def read_csv_employees_file():
    with open ('../homework-1/north_data/employees_data.csv', 'r', encoding='utf-8') as file:
        data = csv.DictReader(file)
        to_db = [(i['employee_id'], i['first_name'], i['last_name'], i['title'], i['birth_date'], i['notes']) for i in data]
        return to_db

def read_csv_orders_file():
    with open ('../homework-1/north_data/orders_data.csv', 'r', encoding='utf-8') as file:
        data = csv.DictReader(file)
        to_db = [(i['order_id'], i['customer_id'], i['employee_id'], i['order_date'], i['ship_city']) for i in data]
        return to_db


def main():
    with psycopg2.connect(host='localhost', database='north', user='postgres', password=432502) as conn:
        with conn.cursor() as cur:
            cur.executemany('INSERT INTO customers VALUES (%s, %s, %s);', (read_csv_customers_file()))
            cur.executemany('INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s);', (read_csv_employees_file()))
            cur.executemany('INSERT INTO orders VALUES (%s, %s, %s, %s, %s);', (read_csv_orders_file()))
            cur.execute('SELECT * FROM customers')
            cur.execute('SELECT * FROM employees')
            cur.execute('SELECT * FROM orders')

            rows = cur.fetchall()
            for row in rows:
                print(row)

    conn.close()


if __name__ == '__main__':
    main()