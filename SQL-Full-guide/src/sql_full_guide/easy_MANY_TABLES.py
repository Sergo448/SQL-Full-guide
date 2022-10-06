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


# Делаем запрос к базе данных, используя обычный SQL-синтаксис
cursor.execute(quiery_7)

# Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
# conn.commit()

results = cursor.fetchall()

print('-----------------')
for s in results:
    print(s)
print('-----------------')
# Не забываем закрыть соединение с базой данных
conn.close()
