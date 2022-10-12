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
             Подзапросы в предложении WHERE
"""

# Вывести список служащих, чей плановый объем продаж
# составляет менее 10% от планового объема продаж всей компании

quiery_1 = f"SELECT NAME FROM SALESREPS" \
           f" WHERE QUOTA < " \
           f" (.1 * (SELECT SUM (TARGET) FROM OFFICES));"
quiery_1_2 = f"SELECT NAME FROM SALESREPS" \
             f" WHERE QUOTA < (SELECT (SUM(TARGET) * 0.1) FROM OFFICES);"

# Вывести список офисов, в которых плановый объем продаж
# превышает сумму плановых объемов продаж всех служащих
quiery_2 = f"SELECT CITY FROM OFFICES " \
           f" WHERE TARGET > " \
           f" (SELECT SUM(QUOTA) FROM SALESREPS WHERE REP_OFFICE = OFFICE);"

# Вывести список офисов, в которых плановый объем продаж
# офиса превышает сумму плановых объемов продаж всех служащих
quiery_3 = f"SELECT CITY FROM OFFICES " \
           f" WHERE TARGET > " \
           f" (SELECT SUM(QUOTA) FROM SALESREPS WHERE REP_OFFICE = OFFICE);"  # OFFICE - внешняя ссылка

"""
            Сравнения с результатом подзапроса
            =
            <>
            <
            <=
            >
            >=
"""

# Вывести список служащих, у которых плановый объем продаж
# не меньше планового объема продаж офиса в Атланте
quiery_4 = f"SELECT NAME FROM SALESREPS" \
           f" WHERE QUOTA >= " \
           f" (SELECT TARGET FROM OFFICES WHERE CITY = 'Atlanta');"

# Вывести список имеющихся в наличии товаров от компании ACI,
# количество которых превышает количество товара ACI-41004
quiery_5 = f"SELECT DESCRIPTION, QTY_ON_HAND FROM PRODUCTS" \
           f" WHERE MFR_ID = 'ACI'" \
           f" AND QTY_ON_HAND > " \
           f"   (SELECT QTY_ON_HAND FROM PRODUCTS " \
           f"    WHERE MFR_ID = 'ACI' " \
           f"    AND PRODUCT_ID = '41004')" \
           f" GROUP BY QTY_ON_HAND;"
"""
        Не все СУБД позволяют иметь подзапрос с левой стороны от части сравнения
"""

# IN or NOT IN
# Вывести список служащих тех офисов, где фактический объем продаж превышает плановый
quiery_6 = f"SELECT NAME FROM SALESREPS" \
           f" WHERE REP_OFFICE IN" \
           f"   (SELECT OFFICE FROM OFFICES WHERE SALES > TARGET);"

# Вывести список всех клиентов, заказавших изделия компании ACI
# (производитель ACI, идентификаторы товаров начинаются с 4100)
# в период между январем и июнем 2008 года
quiery_7 = f"SELECT COMPANY FROM CUSTOMERS" \
           f" WHERE CUST_NUM IN" \
           f"   (SELECT DISTINCT CUST FROM ORDERS" \
           f"    WHERE MFR = 'ACI' " \
           f"       AND PRODUCT LIKE '4100%'" \
           f"       AND ORDER_DATE BETWEEN '2008-01-01'" \
           f"                      AND '2008-06-30');"

"""
            EXISTS() - проверка существования
            Проверка на существование допустима только в подзапросах
            Допускается использования SELECT(*) в подзапросе
"""

"""
Есть два запроса
1) Вывести список товаров, на которые получен заказ стоимостью не менее 25000
Данный запрос можно перефразировать и получить следующий
2) Вывести список товаров, для которых в таблице ORDERS существует по крайней ере один заказ,
который а) является заказом на данный товар; б) имеет стоимость не менее 25 000.
"""
# Итого
quiery_8 = f"SELECT DISTINCT DESCRIPTION FROM PRODUCTS" \
           f" WHERE EXISTS " \
           f"   (SELECT ORDER_NUM FROM ORDERS" \
           f"   WHERE PRODUCT = PRODUCT_ID " \
           f"   AND MFR = MFR_ID" \
           f"   AND AMOUNT >= 25000.00);"

quiery_8_1 = f"SELECT DISTINCT DESCRIPTION FROM PRODUCTS" \
           f" WHERE EXISTS " \
           f"   (SELECT * FROM ORDERS" \
           f"   WHERE PRODUCT = PRODUCT_ID " \
           f"   AND MFR = MFR_ID" \
           f"   AND AMOUNT >= 25000.00);"

"""
                ANY(), ALL() Многократное сравнение
                Предикаты используются совместно с одним из шести операторов сравнения
                и сравнивает проверяемое значение со столбцом данных, отобранных запросом
                Проверяемое значение 1) Поочередно сравнивается с каждым элементов (a)ANY, b)ALL)
                Если получаем TRUE то ANY возвращает TRUE, если все сравнения в Б возвращают
                TRUE, то и ALL возвращает TRUE.
                ВМЕСТО ANY МОЖНО ИСПОЛЬЗОВАТЬ SOME
"""
# Вывести список служащих, принявших заказ на сумму, превышающую 10% от плана
quiery_9 = f"SELECT NAME " \
           f" FROM SALESREPS" \
           f" WHERE ((.1 * QUOTA) < ANY (SELECT AMOUNT" \
           f"                               FROM ORDERS" \
           f"                                WHERE REP = EMPL_NUM));"

# Вывести имена и возраст всех служащих, которые не руководят офисами
quiery_10 = f"SELECT NAME, AGE FROM SALESREPS" \
            f" WHERE NOT (EMPL_NUM = ANY (SELECT MGR FROM OFFICES);"

quiery_10_1 = f"SELECT NAME, AGE" \
              f" FROM SALESREPS" \
              f" WHERE NOT EXISTS (SELECT *" \
              f"                    FROM OFFICES" \
              f"                    WHERE EMPL_NUM = MGR)" \
              f" GROUP BY NAME;"

# Вывести список офисов с плановыми объемами продаж, у всех служащих
# которых фактический объем продаж превышает 50 % от плана офиса
quiery_11 = f"SELECT CITY, TARGET FROM OFFICES" \
            f" WHERE (0.50 * TARGET) < ALL " \
            f"      (SELECT SALES FROM SALESREPS" \
            f"      WHERE REP_OFFICE = OFFICE);"

"""
                Подзапросы и соединения
"""
# Вывести имена и возраст служащих, работающих в офисах западного региона
quiery_12 = f"SELECT NAME, AGE" \
            f" FROM SALESREPS" \
            f" WHERE REP_OFFICE IN " \
            f"      (SELECT OFFICE FROM OFFICES" \
            f"      WHERE REGION = 'Western');"
quiery_12_1 = f"SELECT NAME, AGE FROM SALESREPS, OFFICES " \
              f" WHERE REP_OFFICE = OFFICE " \
              f" AND REGION = 'Western';"


# Делаем запрос к базе данных, используя обычный SQL-синтаксис
# cursor.execute(quiery_12)
cursor.execute(quiery_12_1)

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
