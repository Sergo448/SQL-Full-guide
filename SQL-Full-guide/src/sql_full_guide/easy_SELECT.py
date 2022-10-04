# -*- coding: utf-8 -*-
# Sergey.6362@mail.ru

import sqlite3


# создаем подключение к нашей базе данных
conn = sqlite3.connect('./DATA_SQL/DATA_BOOK_A')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ
quiery_1 = "SELECT CITY, TARGET, SALES FROM OFFICES;"

quiery_2 = "SELECT CITY, TARGET, SALES FROM OFFICES WHERE REGION = 'Eastern';"

# Вывести список офисов в восточном регионе, в которых фактические
# объемы продаж превысили плановые. Отсортироовать список в
# алфавитном порядке по названиям городов.
quiery_3 = "SELECT CITY, TARGET, SALES FROM OFFICES WHERE REGION = 'Eastern' AND SALES > TARGET ORDER BY CITY;"

"""
            SELECT & FROM - обязательны
            WHERE - следует включать только некоторые строки  при условии отбора
            GROUP BY - группирует строки базы данных по определенному признаку,
             а затем включает запрос в одну итоговую строку для каждой группы
            HAVING - слудет включать только некоторые из групп, создванных предыдущей функцией
            ORDER BY -  сортирует результаты запроса на основании данных, содержащ. в столбцах
"""

# Вывести список имен, офисов и дат приема на работу всех служащих отсортированных по имени
quiery_4 = "SELECT NAME, REP_OFFICE, HIRE_DATE FROM SALESREPS ORDER BY NAME;"

# No comments...
quiery_5 = "SELECT NAME, QUOTA, SALES FROM SALESREPS WHERE EMPL_NUM = 107;"

# Среднее значение фактических объемов продаж по всем служащим компании
quiery_6 = "SELECT AVG(SALES) FROM SALESREPS;"

# Zero rows
quiery_7 = "SELECT NAME, HIRE_DATE FROM SALESREPS WHERE SALES > 500000.00;"

# Список служащих с их плановым объемом продаж и менеджерами
quiery_8 = "SELECT NAME, QUOTA, MANAGER FROM SALESREPS;"

# Вывести для каждого из офисов список городов, регионов и объемов продаж
quiery_9 = "SELECT CITY, REGION, SALES FROM OFFICES;"

# Для каждого офиса, список городов, регионов и сумм, на которые был перевыполнен/недовыполнен план по продажам
quiery_10 = "SELECT CITY, REGION, (SALES - TARGET) FROM OFFICES;"

# Общая стоимость по каждому товару
quiery_11 = "SELECT MFR_ID, PRODUCT_ID, DESCRIPTION, (QTY_ON_HAND * PRICE) FROM PRODUCTS;"

quiery_12 = "SELECT NAME, QUOTA, (QUOTA + (0.03 * SALES)) FROM SALESREPS;"
# sqlite3 no such function: MONTH(), YEAR(), etc.
# quiery_13 = "SELECT NAME, MONTH(HIRE_DATE), YEAR(HIRE_DATE) FROM SALESREPS;"

# Список объемов продаж для каждого города
quiery_14 = "SELECT CITY, 'has sales of', SALES FROM OFFICES;"

# All *select
quiery_15 = "SELECT * FROM OFFICES;"

# ALL but better
quiery_16 = "SELECT OFFICE, CITY, REGION, MGR, TARGET, SALES FROM OFFICES;"

# Список идентификаторов всех менеджеров офисов
quiery_17 = "SELECT MGR FROM OFFICES;"

# quiery_17 but unique
quiery_18 = "SELECT DISTINCT MGR FROM OFFICES;"

"""
            Далее запросы с уловием WHERE
            
            Различные условия...
"""

quiery_19 = "SELECT CITY, SALES, TARGET FROM OFFICES WHERE SALES > TARGET;"
quiery_20 = "SELECT NAME, SALES, QUOTA FROM SALESREPS WHERE EMPL_NUM = 105;"
quiery_21 = "SELECT NAME, SALES FROM SALESREPS WHERE MANAGER = 104;"

"""
            Условия отбора:
            1) Сравнение =, <> (!=), <, >, >=, <=
            2) Проверка на принадлежность диапазону
            3) Проверка наличия во множестве
            4) Проверка на соответствие шаблону
            5) Проверка на равенство значению NULL 
"""
quiery_22 = "SELECT NAME FROM SALESREPS WHERE HIRE_DATE < '2006-01-01';"
quiery_23 = "SELECT CITY, SALES, TARGET FROM OFFICES WHERE SALES < (.8 * TARGET);"
quiery_24 = "SELECT CITY, MGR FROM OFFICES WHERE MGR <> 108;"
quiery_25 = "SELECT COMPANY, CREDIT_LIMIT FROM CUSTOMERS WHERE CUST_NUM = 2107;"
quiery_26 = "SELECT NAME FROM SALESREPS WHERE SALES > QUOTA;"
quiery_27 = "SELECT NAME FROM SALESREPS WHERE SALES < QUOTA;"

# Using for being in interval BETWEEN ... AND...

quiery_28 = f"SELECT ORDER_NUM, ORDER_DATE, MFR, PRODUCT, AMOUNT" \
            f" FROM ORDERS" \
            f" WHERE ORDER_DATE BETWEEN '2007-10-01' AND '2007-12-31';"

quiery_29 = f"SELECT ORDER_NUM, AMOUNT FROM ORDERS WHERE AMOUNT BETWEEN 20000.00 AND 29999.99;"
quiery_30 = f"SELECT ORDER_NUM, AMOUNT FROM ORDERS WHERE AMOUNT BETWEEN 30000.00 AND 39999.99;"
quiery_31 = f"SELECT ORDER_NUM, AMOUNT FROM ORDERS WHERE AMOUNT BETWEEN 40000.00 AND 49999.99;"

# Using IN

quiery_32 = "SELECT NAME, QUOTA, SALES FROM SALESREPS WHERE REP_OFFICE IN (11, 13, 22);"
quiery_33 = f"SELECT ORDER_NUM, ORDER_DATE, AMOUNT FROM ORDERS " \
            f"WHERE ORDER_DATE IN ('2008-01-04', '2008-01-11', '2008-02-25', '2008-01-25');"
quiery_34 = "SELECT ORDER_NUM, REP, AMOUNT FROM ORDERS WHERE REP IN (107, 109, 101, 103);"

# Using LIKE ESCAPE

quiery_35 = "SELECT COMPANY, CREDIT_LIMIT FROM CUSTOMERS WHERE COMPANY = 'Smithson Corp.';"
"""
            % - совпаадет с любой последовательсностью из нуля или более символов
            _ - соотвевтствует совпаденю с любым отдельным символом
"""
quiery_36 = "SELECT COMPANY, CREDIT_LIMIT FROM CUSTOMERS WHERE COMPANY LIKE 'Smith% Corp.';"
quiery_37 = "SELECT COMPANY, CREDIT_LIMIT FROM CUSTOMERS WHERE COMPANY LIKE 'Smith_n Corp.';"
quiery_38 = "SELECT COMPANY, CREDIT_LIMIT FROM CUSTOMERS WHERE COMPANY LIKE 'Smiths_n %';"
quiery_39 = "SELECT ORDER_NUM, PRODUCT FROM ORDERS WHERE PRODUCT LIKE 'A$%BC%' ESCAPE '$';"

# Using NULL (IS NULL)

quiery_40 = "SELECT NAME FROM SALESREPS WHERE REP_OFFICE IS NULL;"
quiery_41 = "SELECT NAME FROM SALESREPS WHERE REP_OFFICE IS NOT NULL;"

# AND OR NOT
"""
                Операторы по приоритету сверху вниз:
                1) NOT
                2) AND
                3) OR
                Using () make code better to understand
                
                ПОМИМО ОСТАЛЬНОГО ПОЯВИЛИСЬ ОПЕРАТОРЫ
                (...) IS (TRUE / FALSE / UNKNOWN)
                Пример:
                ((SALES - QUOTA) > 10000.00) IS UNKNOWN
                ((SALES - QUOTA) > 10000.00) IS FALSE
                else:
                NOT ((SALES - QUOTA) > 10000.00)
"""
quiery_42 = "SELECT NAME, QUOTA, SALES FROM SALESREPS WHERE SALES < QUOTA OR SALES < 300000.00;"
quiery_43 = "SELECT NAME, QUOTA, SALES FROM SALESREPS WHERE SALES < QUOTA AND SALES < 300000.00;"
quiery_44 = "SELECT NAME, QUOTA, SALES FROM SALESREPS WHERE SALES < QUOTA AND NOT SALES < 300000.00;"
quiery_45 = f"SELECT NAME FROM SALESREPS WHERE (REP_OFFICE IN (22, 11, 12))" \
            f"OR  (MANAGER IS NULL AND HIRE_DATE >= '2006-06-01')" \
            f"OR (SALES > QUOTA AND NOT SALES > 600000.00)" \
            f"ORDER BY NAME;"

"""
                    SORTING USING
                    ORDER BY()
                    По умолчанию по возрастанию
                    Для сортировки по убыванию следует включить в предложение ключь DESC
                    Else ASC
"""
quiery_46 = "SELECT CITY, REGION, SALES FROM OFFICES ORDER BY REGION, CITY;"
quiery_47 = "SELECT CITY, REGION, SALES FROM OFFICES ORDER BY SALES DESC;"
quiery_48 = "SELECT CITY, REGION, (SALES - TARGET) FROM OFFICES ORDER BY (SALES - TARGET) DESC;"
quiery_49 = "SELECT CITY, REGION, (SALES - TARGET) FROM OFFICES ORDER BY REGION ASC, 3 DESC;"

"""
                Using (0UNION)*
                Объединение результатов нескольких запросов
"""

# Вывести список всех товаро, цена которых превышает 2000$ или
# которых было заказано болеее чем на 30 000$ за 1 раз
quiery_50_1 = "SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS WHERE PRICE > 2000.00;"
quiery_50_2 = "SELECT DISTINCT MFR, PRODUCT FROM ORDERS WHERE ANOUNT > 30000.00;"
# OR CAN BE
quiery_51 = (f"SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS WHERE PRICE > 2000.00"
             f" UNION"
             f" SELECT DISTINCT MFR, PRODUCT FROM ORDERS WHERE AMOUNT > 30000.00;")

# Вывести список всех товаров, цена которых превышает 2000 или которых
# было заказано более чем на 30000 за 1 раз
quiery_52 = (f"SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS WHERE PRICE > 2000.00"
             f" UNION ALL"
             f" SELECT DISTINCT MFR, PRODUCT FROM ORDERS WHERE AMOUNT > 30000.00;")

# Вывести список всех товаров, цена которых превышает 2000 или которых было заказано более
# чем на 30 000 за 1 раз. Список отсортировать по наименованию производителя и номеру товара
quiery_53 = (f"SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS WHERE PRICE > 2000.00"
             f" UNION"
             f" SELECT DISTINCT MFR, PRODUCT FROM ORDERS WHERE AMOUNT > 30000.00"
             f" ORDER BY 1, 2;")

# ВЛОЖАННЫЕ ОБЪЕДИНЕНИЯ *
# quiery_54 = (f"SELECT * FROM A UNION (SELECT * FROM B UNION SELECT * FROM C;")

# Делаем запрос к базе данных, используя обычный SQL-синтаксис
cursor.execute(quiery_53)

# !------------------!------------------!------------------!------------------!------------------!
# Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
# conn.commit()
# !------------------!------------------!------------------!------------------!------------------!

results = cursor.fetchall()

print('-----------------')
for s in results:
    print(s)
print('-----------------')
# Не забываем закрыть соединение с базой данных
conn.close()
