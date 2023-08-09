-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника, работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London, а доставку заказа ведет компания United Package (company_name в табл shippers)

select customers.company_name, CONCAT(employees.first_name, ' ', employees.last_name) as ФИО
from orders
inner join customers using(customer_id)
left join employees using(employee_id)
where employees.city=customers.city and orders.ship_via='2';


-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.

SELECT product_name, units_in_stock, contact_name, phone
FROM products
JOIN categories USING(category_id)
JOIN suppliers USING(supplier_id)
WHERE category_name IN ('Dairy Products', 'Condiments') AND discontinued = 0 AND units_in_stock < 25
ORDER BY units_in_stock;


-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа

select company_name from customers
WHERE customer_id NOT IN (SELECT customer_id from orders);

-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см в колонке quantity табл order_details)
-- Этот запрос написать именно с использованием подзапроса.

select distinct product_name, product_id from products
where exists (select * from order_details where order_details.product_id=products.product_id and order_details.quantity=10)
order by product_id;