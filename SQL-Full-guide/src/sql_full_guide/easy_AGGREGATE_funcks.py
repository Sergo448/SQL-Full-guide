# -*- coding: utf-8 -*-
# Sergey.6362@mail.ru


import re
import sqlite3

# создаем подключение к нашей базе данных
conn = sqlite3.connect('./DATA_SQL/DATA_BOOK_A')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ

# Перечислить все заказы, включая номер и стоимость заказа, а также имя и лимит
# кредита клиента, сделавшего заказ.
"""
            Типы агрегирующих функций:
            AVG() - принимает столбец и возвращает среднее значение для столбца (пр. quiery_1)
            SUM() - принимает столбец и возвращает сумму значений столбца (пр. quiery_3)
            MIN() - принимает столбец и возвращает минимальное значение для столбца (пр. quiery_7)
            MAX() - принимает столбец и возвращает максимальное значение для столбца (пр. quiery_7_3)
            COUNT() - принимает столбец и возвращает количество значенией для столбца (пр. quiery_8)
            COUNT() не учитывает значения NULL, их учитывает функция COUNT(*)
            COUNT(*) - подсчитывает количество строк в таблице результатов запроса (пр. quiery_10_3)
            
            
"""
quiery_1 = "SELECT AVG(QUOTA), AVG(SALES) FROM SALESREPS"
quiery_2 = "SELECT AVG(100 * (SALES / QUOTA)) FROM SALESREPS;"

quiery_3 = "SELECT SUM(QUOTA), SUM(SALES) FROM SALESREPS"
quiery_4 = "SELECT SUM(AMOUNT) FROM ORDERS, SALESREPS WHERE NAME = 'Bill Adams' AND REP = EMPL_NUM;"

quiery_5 = "SELECT AVG (PRICE) FROM PRODUCTS WHERE MFR_ID = 'ACI';"
quiery_6 = "SELECT AVG(AMOUNT) FROM ORDERS WHERE CUST = 2103;"

quiery_7 = "SELECT MIN(QUOTA), MAX(QUOTA) FROM SALESREPS;"
quiery_7_2 = "SELECT MAX(100 * (SALES/QUOTA)) FROM SALESREPS;"
quiery_7_3 = "SELECT MAX (SALES) FROM SALESREPS;"

quiery_8 = "SELECT COUNT (CUST_NUM) FROM CUSTOMERS;"
quiery_9 = "SELECT COUNT(NAME) FROM SALESREPS WHERE SALES > QUOTA;"
quiery_10 = "SELECT COUNT(AMOUNT) FROM ORDERS WHERE AMOUNT > 25000.00;"
quiery_10_2 = "SELECT COUNT(ORDER_NUM) FROM ORDERS WHERE AMOUNT > 25000.00;"
quiery_10_3 = "SELECT COUNT(*) FROM ORDERS WHERE AMOUNT > 25000.00;"

# Найти среднюю стоимость заказов, общую стоимость заказов, среднюю
# стоимость заказов в процентах от лимита кредитов клиентов, а также среднюю
# стоимость заказов в процентах от плановых объемов продаж служащих
quiery_11 = f"SELECT AVG(AMOUNT), SUM(AMOUNT)," \
            f" (100 * AVG(AMOUNT/CREDIT_LIMIT)), " \
            f" (100 * AVG(AMOUNT/QUOTA)) " \
            f" FROM ORDERS, CUSTOMERS, SALESREPS " \
            f" WHERE CUST = CUST_NUM " \
            f" AND REP = EMPL_NUM;"
quiery_11_2 = f"SELECT AMOUNT, AMOUNT, AMOUNT/CREDIT_LIMIT, AMOUNT/QUOTA" \
              f" FROM ORDERS, CUSTOMERS, SALESREPS" \
              f" WHERE CUST = CUST_NUM " \
              f" AND REP = EMPL_NUM;"
quiery_12 = "SELECT COUNT(*), COUNT(SALES), COUNT(QUOTA) FROM SALESREPS;"

quiery_13 = "SELECT SUM(SALES), SUM(QUOTA), (SUM(SALES)-SUM(QUOTA)), SUM(SALES-QUOTA) FROM SALESREPS;"


# DISTINCT
quiery_14 = "SELECT COUNT(DISTINCT TITLE) FROM SALESREPS;"
quiery_15 = "SELECT COUNT(DISTINCT REP_OFFICE) FROM SALESREPS WHERE SALES > QUOTA;"

# GROUP BY
quiery_16 = "SELECT AVG(AMOUNT) FROM ORDERS;"
quiery_17 = "SELECT REP, AVG(AMOUNT) FROM ORDERS GROUP BY REP;"
quiery_18 = "SELECT REP_OFFICE, MIN(QUOTA), MAX(QUOTA) FROM SALESREPS GROUP BY (REP_OFFICE);"
quiery_19 = "SELECT REP_OFFICE, COUNT(*) FROM SALESREPS GROUP BY REP_OFFICE;"
quiery_20 = "SELECT COUNT(DISTINCT CUST_NUM), 'customers for salesrep', CUST_REP FROM CUSTOMERS GROUP BY CUST_REP;"
quiery_21 = "SELECT REP, CUST, SUM(AMOUNT) FROM ORDERS GROUP BY REP, CUST;"

# WITH ROLLUP - выводит промежуточные итоги для каждого уровня группировки
# WITH CUBE - показывает результаты для каждой возможной комбинации столбцов группировки
quiery_22 = f"SELECT REP, CUST, SUM(AMOUNT) AS RES" \
            f" FROM ORDERS" \
            f" GROUP BY REP, WITH ROLLUP CUST;"
quiery_23 = f"SELECT REP, CUST, SUM(AMOUNT)" \
            f" FROM ORDERS " \
            f" GROUP BY CUBE, CUST WITH CUBE;"
quiery_24 = f"SELECT CUST, REP, SUM(AMOUNT) " \
            f" FROM ORDERS " \
            f" GROUP BY CUST, REP" \
            f" ORDER BY CUST, REP;"
quiery_25 = f"SELECT EMPL_NUM, NAME, SUM(AMOUNT) " \
            f" FROM ORDERS, SALESREPS" \
            f" WHERE REP = EMPL_NUM " \
            f" GROUP BY EMPL_NUM;"
quiery_26 = f"SELECT EMPL_NUM, NAME, SUM(AMOUNT) " \
            f" FROM ORDERS, SALESREPS" \
            f" WHERE REP = EMPL_NUM " \
            f" GROUP BY EMPL_NUM, NAME;"
quiery_27 = f"SELECT NAME, SUM(AMOUNT) " \
            f" FROM ORDERS, SALESREPS" \
            f" WHERE REP = EMPL_NUM " \
            f" GROUP BY NAME;"


# HAVING()
# Какова средняя стоимость заказа для каждого служащего из числа тех, у которых
# общая стоимость заказов превышает 30 000?
quiery_28 = f"SELECT REP, AVG(AMOUNT) " \
            f" FROM ORDERS" \
            f" GROUP BY REP" \
            f" HAVING SUM(AMOUNT) > 30000.00;"
quiery_29 = "SELECT CITY, SUM(QUOTA), SUM(SALESREPS.SALES)" \
            " FROM OFFICES, SALESREPS" \
            " WHERE OFFICE = REP_OFFICE" \
            " GROUP BY CITY" \
            " HAVING COUNT(*) >= 2;"
# Показать цену, количество на складе и общее количество заказанных единиц для
# каждого наименования товара, если для него общее количество заказанных единиц
# превышали 75 процентов от количества товаров на складе
quiery_30 = "SELECT DESCRIPTION, PRICE, QTY_ON_HAND, SUM(QTY)" \
            " FROM PRODUCTS, ORDERS" \
            " WHERE MFR = MFR_ID" \
            " AND PRODUCT = PRODUCT_ID" \
            " GROUP BY MFR_ID, PRODUCT_ID, DESCRIPTION, PRICE, QTY_ON_HAND" \
            " HAVING SUM(QTY) > (0.75 * QTY_ON_HAND)" \
            " ORDER BY QTY_ON_HAND DESC;"

# Делаем запрос к базе данных, используя обычный SQL-синтаксис
# cursor.execute(quiery_12)
cursor.execute(quiery_30)

# !------------------!------------------!------------------!------------------!------------------!
# Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
# conn.commit()
# !------------------!------------------!------------------!------------------!------------------!

results = cursor.fetchall()
print('SQL quiery result:')
print('-----------------')
for s in results:
    print(s)
print('-----------------')
# Не забываем закрыть соединение с базой данных
conn.close()
