# -*- coding: utf-8 -*-
# Sergey.6362@mail.ru


import re
import sqlite3


# создаем подключение к нашей базе данных
conn = sqlite3.connect('./DATA_SQL/DATA_BOOK_A', timeout=10)

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
quiery_6 = f"INSERT OR IGNORE INTO BIGORDERS (AMOUNT, COMPANY, NAME, PERF, PRODUCT, MFR, QTY)" \
           f" SELECT AMOUNT, COMPANY, NAME, (SALES - QUOTA), PRODUCT, MFR, QTY" \
           f" FROM ORDERS, CUSTOMERS, SALESREPS" \
           f" WHERE CUST = CUST_NUM" \
           f" AND REP = EMPL_NUM" \
           f" AND AMOUNT > 15000.00;"

"""
            DELETE()
"""

quiery_7 = f"DELETE FROM SALESREPS" \
           f" WHERE NAME = 'Henry Jacobsen';"
quiery_8 = f"DELETE FROM ORDERS WHERE CUST = 2126;"
quiery_9 = f"DELETE FROM ORDERS WHERE ORDER_DATE < '2007-11-15;"
quiery_10 = f"DELETE FROM CUSTOMERS WHERE CUST_REP IN (105, 109, 101);"
quiery_11 = f"DELETE FROM SALESREPS WHERE HIRE_DATE < '2006-07-01' AND QUOTA IS NULL;"
quiery_12 = f"DELETE FROM ORDERS;"

quiery_13 = f"DELETE FROM ORDERS " \
            f" WHERE REP = (SELECT EMPL_NUM FROM SALESREPS WHERE NAME = 'Sue Smith');"
quiery_14 = f"DELETE FROM CUSTOMERS WHERE CUST_REP IN" \
            f" (SELECT EMPL_NUM FROM SALESREPS WHERE SALES < (0.8 * QUOTA));"
quiery_15 = f"DELETE FROM SALESREPS" \
            f" WHERE (0.02 * QUOTA) > (SELECT SUM(AMOUNT) FROM ORDERS WHERE REP = EMPL_NUM);"
quiery_16 = f"DELETE FROM CUSTOMERS " \
            f" WHERE NOT EXISTS " \
            f"      (SELECT * FROM ORDERS" \
            f"          WHERE CUST = CUST_NUM AND ORDER_DATE > '2007-11-10');"
"""
            UPDATE()
"""

quiery_17 = f"UPDATE CUSTOMERS SET CREDIT_LIMIT = 60000.00, CUST_REP = 109 WHERE COMPANY = 'Acme Mfg.';"

quiery_18 = f"UPDATE SALESREPS SET REP_OFFICE = 11, QUOTA = .9 * QUOTA WHERE REP_OFFICE = 12;"

quiery_19 = f"UPDATE CUSTOMERS SET CUST_REP = 102 WHERE CUST_REP IN (105, 106, 107);"
quiery_20 = f"UPDATE SALESREPS SET QUOTA = 10000.00 WHERE QUOTA IS NULL;"
quiery_21 = f"UPDATE SALESREPS SET QUOTA = 1.05 * QUOTA;"

quiery_22 = f"UPDATE CUSTOMERS " \
            f" SET CREDIT_LIMIT = CREDIT_LIMIT + 5000.0" \
            f" WHERE CUST_NUM IN (" \
            f"  SELECT DISTINCT CUST FROM ORDERS WHERE AMOUNT > 25000.00" \
            f" );"

quiery_23 = f"UPDATE CUSTOMERS SET CUST_REP = 105" \
            f" WHERE CUST_REP IN" \
            f" (SELECT EMPL_NUM FROM SALESREPS WHERE SALES < (0.8 * QUOTA));"

quiery_24 = f"UPDATE SALESREPS SET MANAGER = 106" \
            f" WHERE 3 < (SELECT COUNT(*) FROM CUSTOMERS WHERE CUST_REP = EMPL_NUM);"


# Делаем запрос к базе данных, используя обычный SQL-синтаксис
# cursor.execute(quiery_12)
cursor.execute(quiery_24)

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
