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
quiery_12_2 = f"SELECT NAME, AGE FROM SALESREPS" \
              f" WHERE EXISTS " \
              f"    (SELECT * FROM OFFICES" \
              f"        WHERE REGION = 'Western'" \
              f"        AND REP_OFFICE = OFFICE);"

"""
            ВЛОЖЕННЫЕ ПОДЗАПРОСЫ
"""

# Вывести список клиентов, закрепленных за служащими, работающими в офисах восточного региона
quiery_13 = f"SELECT COMPANY" \
            f" FROM CUSTOMERS" \
            f"  WHERE CUST_REP IN (SELECT EMPL_NUM" \
            f"                      FROM SALESREPS" \
            f"                      WHERE REP_OFFICE IN (SELECT OFFICE " \
            f"                                              FROM OFFICES" \
            f"                                              WHERE REGION = 'Eastern'));"

"""
                КОРРЕЛИРОВАННЫЕ ПОДЗАПРОСЫ
                
                подзапросы зависят от внешней ссылки (коррелированной ссылки)
                т.о. такие подзапросы становятся корредированными с каждой
                строчкой таблицы главного запроса
                 
"""
# Вывести список руководителей старше 40 лет, у которых есть служащие,
# опережающие план и работающие со своими руководителями в разных офисах

# Для удобства одна и также таблица в основном запросе и подзапросе имеет разные псевдонимы
quiery_14 = f"SELECT NAME FROM SALESREPS AS MGRS " \
            f" WHERE AGE > 40 " \
            f"  AND MGRS.EMPL_NUM IN (SELECT MANAGER FROM SALESREPS AS EMPS" \
            f"                          WHERE EMPS.SALES > EMPS.QUOTA" \
            f"                          AND EMPS.REP_OFFICE <> MGRS.REP_OFFICE);"

"""
                Подзапросы в предложении HAVING*
"""
# Вывести список служащих, у которых средняя стоимость заказов на товары, изготовленные
# компанией ACI, выше, чем общая средняя стоимость заказов
quiery_15 = f"SELECT NAME, AVG (AMOUNT) FROM SALESREPS, ORDERS" \
            f" WHERE EMPL_NUM = REP" \
            f"  AND MFR = 'ACI'" \
            f"      GROUP BY NAME" \
            f"  HAVING AVG(AMOUNT) > (SELECT AVG(AMOUNT) FROM ORDERS);"

# Вывести список служащих, у каждого из которых средняя стоимость заказов
# на товары, изготовленные компанией ACI, не меньше, чем средняя
# стоимость заказов этого служащего
quiery_15_1 = f"SELECT NAME, AVG(AMOUNT) FROM SALESREPS, ORDERS" \
              f" WHERE EMPL_NUM = REP" \
              f"    AND MFR = 'ACI'" \
              f"    GROUP BY NAME, EMPL_NUM" \
              f" HAVING AVG(AMOUNT) >= (SELECT AVG(AMOUNT) FROM ORDERS" \
              f"                        WHERE REP = EMPL_NUM);"


"""
        CAST(),
         - Для преобразования данных из таблицы, в которой столбец
         определен с неверным типом данных
         - Для приведения возвращаемых запросом данных к типу, 
         поддерживаемому клиентским приложением
         - Для устранения отличий типов данных в двух разных таблицах             
         CASE(),
          - Для использования синтаксиса подобного If, then, esle...
          CASE...WHEN...THEN...etc.
         COALESCE() = easier then case
         NULLIF()
         
"""

quiery_16 = f"SELECT NAME, CAST (REP_OFFICE AS CHAR), " \
            f"             CAST (HIRE_DATE AS CHAR)" \
            f"FROM SALESREPS;"

quiery_17 = f"SELECT PRODUCT, QTY, AMOUNT" \
            f" FROM ORDERS" \
            f" WHERE CUST = CAST ('2107' AS INTEGER);"
# Пример. Нам нужны общие объемы продаж служащих по офисам. Если служащему
# не назначен офис, его сумма должна включаться в итог по офису его руководителя
quiery_18 = f"SELECT CITY, SUM(SALESREPS.SALES) " \
            f" FROM OFFICES, SALESREPS" \
            f"  WHERE OFFICE = CASE WHEN (REP_OFFICE IS NOT NULL) " \
            f"                      THEN REP_OFFICE " \
            f"                      ELSE (SELECT REP_OFFICE" \
            f"                          FROM SALESREPS AS MGRS" \
            f"                          WHERE MGRS.EMPL_NUM = MANAGER)" \
            f"                  END" \
            f"  GROUP BY CITY; "

quiery_19 = f"SELECT NAME, CITY, " \
            f"      CASE OFFICE WHEN 11 THEN 'New York'" \
            f"                  WHEN 12 THEN 'Illinois'" \
            f"                  WHEN 13 THEN 'Georgia'" \
            f"                  WHEN 21 THEN 'California'" \
            f"                  WHEN 22 THEN 'Colorado'" \
            f"      END AS STATE" \
            f" FROM OFFICES, SALESREPS" \
            f" WHERE MGR = EMPL_NUM;"

quiery_20 = f"SELECT NAME, CASE WHEN (QUOTA IS NOT 'NULL' OR NULL) THEN QUOTA" \
            f"                  WHEN (SALES IS NOT NULL OR 'NULL') THEN SALES" \
            f"                  ELSE 0.00" \
            f"                  END AS ADJUSTED_QUOTA" \
            f"  FROM SALESREPS"

quiery_21 = f"SELECT NAME, COALESCE(QUOTA, SALES, 0.00) FROM SALESREPS;"
quiery_22 = f"SELECT CITY, SUM(SALESREPS.SALES) FROM OFFICES, SALESREPS" \
            f" WHERE OFFICE = NULLIF (REP_OFFICE, 0)" \
            f" GROUP BY CITY;"

"""
                Выражения со строками таблиц
                (выражение) к какой-то таблице с выбранными строками,
                 которые совпадают со значениями в выражении
"""


# Перечислить номера заказов на изделие ACI 41002 с указанием количества единиц товара и суммы сделки
quiery_23 = f"SELECT ORDER_NUM, QTY, AMOUNT FROM ORDERS WHERE (MFR, PRODUCT) = ('ACI', '41002');"
quiery_23_1 = f"SELECT ORDER_NUM, QTY, AMOUNT FROM ORDERS" \
              f" WHERE (MFR = 'ACI') AND (PRODUCT = '41002');"

"""
            Подзапросы, возвращающие строки
"""
quiery_24 = f"SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS" \
            f" WHERE PRICE = (SELECT MAX(PRICE) FROM PRODUCTS);"
quiery_25 = f"SELECT ORDER_NUM, ORDER_DATE FROM ORDERS" \
            f" WHERE (MFR, PRODUCT) = (SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS" \
            f"                          WHERE PRICE = (SELECT MAX(PRICE)" \
            f"                                         FROM PRODUCTS));"

"""
                    Табличные выражения
"""

quiery_26 = f"INSERT INTO OFFICES (OFFICE, CITY, REGION, MGR, SALES)" \
            f" VALUES (23, 'San Diego', 'Western', 108, 0.00)," \
            f"        (24, 'Seattle', 'Western', 104, 0.00)," \
            f"        (14, 'Boston', 'Eastern', NULL, 0.00);"
quiery_26_1 = f"SELECT * FROM OFFICES;"

# quiery_26 может включать в своей инструкции и подзапрос

quiery_27 = f"SELECT DESCRIPTION, PRICE FROM PRODUCTS" \
            f" WHERE (MFR_ID, PRODUCT_ID) IN" \
            f"      (SELECT MFR, PRODUCT FROM ORDERS WHERE AMOUNT > 20000.00);"
quiery_27_1 = f"SELECT DISTINCT DESCRIPTION, PRICE FROM PRODUCTS, ORDERS" \
              f" WHERE (MFR_ID = MFR) AND (PRODUCT_ID = PRODUCT) AND (AMOUNT > 20000.00);"

"""
        JOIN() - из двух входных таблиц создает выходную таблицу результатов запроса 
        в соответствии с спецификацией соединения
        UNION() - из двух входных таблиц создает выходную объединенную таблицу результатов запроса
        EXCEPT() - Из двух входных таблиц получает выходную, содержащую все строки, 
        которые имеются в 1й, но отсутствуют во 2й.
        INTERSECT() - Генерирует выходную таблицу из двух входных, содержащую все строки,
        которые имеются в двух входных таблицах.
"""

quiery_28 = f"(SELECT MFR, PRODUCT FROM ORDERS" \
            f"  WHERE AMOUNT > 30000.00) " \
            f" UNION" \
            f"(SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS " \
            f"  WHERE (PRICE * QTY_ON_HAND) > 30000);"
quiery_29 = f"(SELECT MFR, PRODUCT FROM ORDERS" \
            f"  WHERE AMOUNT > 30000.00) " \
            f" INTERSECT" \
            f"(SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS " \
            f"  WHERE (PRICE * QTY_ON_HAND) > 30000);"
quiery_30 = f"(SELECT MFR, PRODUCT FROM ORDERS" \
            f"  WHERE AMOUNT > 30000.00) " \
            f" EXCEPT" \
            f"(SELECT MFR_ID, PRODUCT_ID FROM PRODUCTS " \
            f"  WHERE PRICE < 100.00);"


# Запросы в предложении FROM
# Вывести имена и общие суммы заказов для всех клиентов, чей лимит кредита больше 50 000
quiery_31 = f"SELECT COMPANY, TOT_ORDERS " \
            f" FROM CUSTOMERS, (SELECT CUST, SUM(AMOUNT) AS TOT_ORDERS FROM ORDERS GROUP BY CUST)" \
            f" WHERE (CREDIT_LIMIT > 50000.00)" \
            f" AND (CUST_NUM = CUST); "

# Делаем запрос к базе данных, используя обычный SQL-синтаксис
# cursor.execute(quiery_12)
cursor.execute(quiery_31)

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
