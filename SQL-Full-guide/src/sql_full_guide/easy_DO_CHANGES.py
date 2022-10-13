# -*- coding: utf-8 -*-
# Sergey.6362@mail.ru


import re
import sqlite3

# создаем подключение к нашей базе данных
conn = sqlite3.connect('./DATA_SQL/DATA_BOOK_A')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ

"""
            INSERT () - Добавляет новые строки в таблицу
            DELETE () - Удаляет строки из таблицы
            UPDATE () - Изменяет существующие данные в таблице
"""

# ИНСТРУКЦИЯ INSERT()

# Однострочная INSERT () для добавления одной новой строки
quiery_1 = f"INSERT INTO SALESREPS" \
           f" (NAME, AGE, EMPL_NUM, SALES, TITLE, HIRE_DATE, REP_OFFICE) " \
           f" VALUES" \
           f" ('Henry Jacobsen', 36, 111, 0.00, 'Sales Mgr', '2008-07-25', 13);"
quiery_1_1 = f"SELECT * FROM SALESREPS WHERE NAME = 'Henry Jacobsen';"

quiery_2 = f"INSERT INTO CUSTOMERS " \
           f"(COMPANY, CUST_NUM, CREDIT_LIMIT, CUST_REP)" \
           f" VALUES ('InterCorp', 2126, 15000.00, 111);"
quiery_3 = f"INSERT INTO ORDERS " \
           f"(AMOUNT, MFR, PRODUCT, QTY, ORDER_DATE, ORDER_NUM, CUST, REP)" \
           f" VALUES" \
           f"(2340.00, 'ACI', '41004', 20, CURRENT_DATE, 113070, 2126, 111);"
quiery_4 = f"INSERT INTO SALESREPS " \
           f"(NAME, AGE, EMPL_NUM, SALES, TITLE, HIRE_DATE, REP_OFFICE)" \
           f" VALUES" \
           f"('Henry Jacobsen', 36, 111, 0.00, 'Sales Mgr', '2008-07-25', 13);"
quiery_4_1 = f"INSERT INTO SALESREPS " \
            f"(NAME, AGE, EMPL_NUM, SALES, QUOTA, TITLE, MANAGER, HIRE_DATE, REP_OFFICE)" \
            f" VALUES" \
            f"('Henry Jacobsen', 36, 111, 0.00, NULL, 'Sales Mgr', NULL, '2008-07-25', 13);"
quiery_4_2 = f"INSERT INTO SALESREPS " \
             f" VALUES" \
             f"(111, 'Henry Jacobsen', 36, 13, 'Sales Mgr', '2008-07-25', NULL, NULL, 0.00);"

# МНОГОСТРОЧНА INSERT()
quiery_5 = f"INSERT INTO OLDORDERS (ORDER_NUM, ORDER_DATE, AMOUNT)" \
           f" SELECT ORDER_NUM, ORDER_DATE, AMOUNT FROM ORDERS" \
           f" WHERE ORDER_DATE < '2008-01-01';"




# Делаем запрос к базе данных, используя обычный SQL-синтаксис
# cursor.execute(quiery_12)
cursor.execute(quiery_4)

# !------------------!------------------!------------------!------------------!------------------!
# Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
conn.commit()
# !------------------!------------------!------------------!------------------!------------------!

results = cursor.fetchall()
print('SQL quiery result:')
print('-----------------')
for s in results:
    print(s)
print('-----------------')
# Не забываем закрыть соединение с базой данных
conn.close()
