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

quiery_1 = "SELECT ORDER_NUM, AMOUNT, COMPANY, CREDIT_LIMIT FROM ORDERS, CUSTOMERS WHERE CUST = CUST_NUM;"

# Использование структуры предок - потомок!
# Вывести список всех служащих с городами и регионами, в которых они работают.
# SALESREPS - Потомок, OFFICES - Предок в данном случае
quiery_2 = "SELECT NAME, CITY, REGION FROM SALESREPS, OFFICES WHERE REP_OFFICE = OFFICE;"
quiery_4 = "SELECT NAME, CITY, REGION FROM SALESREPS JOIN OFFICES ON REP_OFFICE = OFFICE;"

# Вывести список офисов с именами и должностями их руководителей
quiery_3 = "SELECT CITY, NAME, TITLE FROM OFFICES, SALESREPS WHERE MGR = EMPL_NUM;"
quiery_5 = "SELECT CITY, NAME, TITLE FROM OFFICES JOIN SALESREPS ON MGR = EMPL_NUM;"

# Соединение с условием отбора
quiery_6 = "SELECT CITY, NAME, TITLE FROM OFFICES, SALESREPS WHERE MGR = EMPL_NUM AND TARGET > 600000.00;"
quiery_7 = "SELECT CITY, NAME, TITLE FROM OFFICES JOIN SALESREPS ON (MGR = EMPL_NUM) WHERE (TARGET > 600000.00); "

# Несколько связных столбцов
# Вывести список всех заказов, включая стоимости и описания товаров
quiery_8 = "SELECT ORDER_NUM, AMOUNT, DESCRIPTION FROM ORDERS, PRODUCTS WHERE MFR = MFR_ID AND PRODUCT = PRODUCT_ID;"
quiery_9 = f"SELECT ORDER_NUM, AMOUNT, DESCRIPTION FROM ORDERS JOIN PRODUCTS ON ((MFR = MFR_ID) AND (PRODUCT = " \
           f"PRODUCT_ID)) "

# Естественные соединения
quiery_10 = "SELECT ORDER_NUM, AMOUNT, DESCRIPTION FROM ORDERS NATURAL JOIN PRODUCTS;"
# ПРЕДСТАВИМ ЧТО В ТАБЛИЦЕ ПРОДУКТС MFR_ID = MFR из ОРДЕРС, но по факту так не является
quiery_11 = "SELECT ORDER_NUM, AMOUNT, DESCRIPTION FROM ORDERS JOIN PRODUCTS USING (MFR, PRODUCTS);"
quiery_12 = f"SELECT ORDER_NUM, AMOUNT, DESCRIPTION FROM ORDERS JOIN PRODUCTS ON ORDERS.MFR = PRODUCTS.MFR_ID AND " \
            f"ORDERS.PRODUCT = PRODUCTS.PRODUCT_ID; "
# ПРЕДПОЧТИТЕЛЬНЕЕ ИСПОЛЬЗОВАТЬ ИНСТРУКЦИЮ USING()

# ЗАПРОСЫ К ТРЕМ И БОЛЕЕ ТАБЛИЦАМ

# Вывести список заказов стоимостью выше 25 000, включающий имя служащего,
# принявшего заказ, и имя клиента, сделавшего его.
quiery_13 = f"SELECT ORDER_NUM, AMOUNT, COMPANY, NAME FROM ORDERS, CUSTOMERS, SALESREPS WHERE CUST = CUST_NUM AND REP " \
            f"= EMPL_NUM AND AMOUNT > 25000.00; "
quiery_14 = f"SELECT ORDER_NUM, AMOUNT, COMPANY, NAME" \
            f" FROM ORDERS" \
            f" JOIN CUSTOMERS ON CUST = CUST_NUM" \
            f" JOIN SALESREPS ON REP = EMPL_NUM" \
            f" WHERE AMOUNT > 25000.00;"
# Вывести список заказов стоимостью выше 25 000, включающий
# имя клиента, сделавшего заказ, и имя служащего, закрепленного за этим клиентом

quiery_15 = f"SELECT ORDER_NUM, AMOUNT, COMPANY, NAME" \
            f" FROM ORDERS, CUSTOMERS, SALESREPS " \
            f" WHERE CUST = CUST_NUM" \
            f" AND CUST_REP = EMPL_NUM" \
            f" AND AMOUNT > 25000.00;"

# Вывести список заказов стоимостью выше 25000, включающий имя клиента,
# сделавшего заказ, имя закрепленного за ним служащего и офис,
# в котором работает этот служащий.
quiery_16 = f"SELECT ORDER_NUM, AMOUNT, COMPANY, NAME, CITY " \
            f" FROM ORDERS, CUSTOMERS, SALESREPS, OFFICES" \
            f" WHERE CUST = CUST_NUM" \
            f"  AND CUST_REP = EMPL_NUM " \
            f"  AND REP_OFFICE = OFFICE " \
            f"  AND AMOUNT > 25000.00;"

quiery_17 = f"SELECT ORDER_NUM, AMOUNT, ORDER_DATE, NAME " \
            f" FROM ORDERS, SALESREPS " \
            f" WHERE ORDER_DATE = HIRE_DATE;"

quiery_18 = f"SELECT NAME, QUOTA, CITY, TARGET " \
            f" FROM SALESREPS, OFFICES " \
            f" WHERE QUOTA > TARGET;"

quiery_19 = f"SELECT NAME, SALESREPS.SALES, CITY " \
            f" FROM SALESREPS, OFFICES" \
            f" WHERE REP_OFFICE = OFFICE;"

quiery_20 = f"SELECT SALESREPS.*, CITY, REGION FROM SALESREPS, OFFICES" \
            f" WHERE REP_OFFICE = OFFICE;"

# Ссылаемся на одну и туже таблицу
quiery_21 = f" SELECT EMPS.NAME, MGRS.NAME " \
            f" FROM SALESREPS EMPS, SALESREPS MGRS " \
            f" WHERE EMPS.MANAGER = MGRS.EMPL_NUM;"

# Вывести список служащих, планы продаж которых превышают планы их руководителей
quiery_22 = f"SELECT SALESREPS.NAME, SALESREPS.QUOTA, MGRS.QUOTA" \
            f" FROM SALESREPS, SALESREPS MGRS" \
            f" WHERE SALESREPS.MANAGER = MGRS.EMPL_NUM" \
            f" AND SALESREPS.QUOTA > MGRS.QUOTA;"

# Вывести список служащих, которые работают в различных офисах со своими руководителями, включающий
# имена и офисы как служащих, так и их руководителей
quiery_23 = f"SELECT EMPS.NAME, EMP_OFFICE.CITY, MGRS.NAME, MGR_OFFICE.CITY" \
            f" FROM SALESREPS AS EMPS, SALESREPS  AS MGRS," \
            f"      OFFICES EMP_OFFICE, OFFICES MGR_OFFICE" \
            f"  WHERE EMPS.REP_OFFICE = EMP_OFFICE.OFFICE" \
            f"    AND MGRS.REP_OFFICE = MGR_OFFICE.OFFICE " \
            f"    AND EMPS.MANAGER = MGRS.EMPL_NUM" \
            f"    AND EMPS.REP_OFFICE <> MGRS.REP_OFFICE;"

# Вывести имя компании и все заказы клиента номер 2103
quiery_24 = f"SELECT COMPANY, ORDER_NUM, AMOUNT" \
            f" FROM CUSTOMERS JOIN ORDERS" \
            f" ON CUST_NUM = CUST" \
            f" WHERE CUST_NUM = 2103" \
            f" ORDER BY ORDER_NUM;"

quiery_25 = f"SELECT NAME, REP_OFFICE FROM SALESREPS;"
quiery_26 = f"SELECT NAME, CITY FROM SALESREPS JOIN OFFICES ON REP_OFFICE = OFFICE;"
# Вывести список служащих и городов, где они работают
quiery_27 = f"SELECT NAME, CITY FROM SALESREPS LEFT OUTER JOIN OFFICES ON REP_OFFICE = OFFICE;"

"""         LEFT and RIGTH JOIN
            
            Есть таблица А и Б
            Если прибегнуть к левому внешнему соединению А с Б
            получим включение всех несвязных строк первой (А) таблицы,
            дополняя их значениями NULL, но не включает несвязные строки 
            второй (правой) таблицы.
            
            Правое внешнее соединение включает все несвязные строки второй 
            таблицы, дополняя их значениями NULL, но не включая несвязные 
            строки левой таблицы.

"""


# Делаем запрос к базе данных, используя обычный SQL-синтаксис
# cursor.execute(quiery_13)
cursor.execute(quiery_27)


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
