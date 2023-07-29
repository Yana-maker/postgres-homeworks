-- SQL-команды для создания таблиц

CREATE TABLE customers(
	customer_id text primary key,
	"company_name" text NOT NULL,
	"contact_name" text NOT NULL
);

CREATE TABLE employees(
	employee_id int primary key,
	"first_name" text NOT NULL,
	"last_name" text NOT NULL,
	"title" text NOT NULL,
	"birth_date" text NOT NULL,
	"notes" text NOT NULL
);

CREATE TABLE orders(
    order_id INT primary key,
    cust_id text REFERENCES customers(customer_id) NOT NULL,
    empl_id INT REFERENCES employees(employee_id) NOT NULL,
    "order_date" text NOT NULL,
    "ship_city" text NOT NULL
)