# -*- coding: utf-8 -*-
# Sergey.6362@mail.ru
# SQL-Full-guide/src/sql_full_guide/easy_INTEGRITY.py

import re
import sqlite3


# создаем подключение к нашей базе данных
conn = sqlite3.connect('./DATA_SQL/DATA_BOOK_A', timeout=10)

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ

# DOMAIN
"""
CREATE DOMAIN (VALID_EMPLOYEE_ID) INTEGER 
 CHECK (VALUE BETWEEN 101 AND 199);
"""

quiery_1 = """
CREATE TABLE SALESREPS
(EMPL_NUM VALID_EMPLOYEE_ID,
 AGE INTEGER CHECK (AGE >= 21),
 .
 .
 .
 QUOTA DECIMAL (9, 2) CHECK (QUOTA >= 0.00),
 .
 .
 );
"""

quiery_2 = """
            CREATE TABLE OFFICES
                (OFFICE INTEGER NOT NULL,
                 CITY VARCHAR (15) NOT NULL,
                 REGION VARCHAR (10) NOT NULL,
                 MGR VALID_EMPLOYEE_ID,
                 TARGET DECIMAL(9, 2),
                 SALES DECIMAL(9, 2) NOT NULL,
                 .
                 .
                 .
"""

quiery_3 = f"CREATE TABLE ADVISOR_ASSIGNMENTS" \
           f" (STUDENT_NAME VARCHAR (25)," \
           f"  ADVISOR_NAME VARCHAR (25)," \
           f" UNIQUE (STUDENT_NAME, ADVISOR_NAME));"

"""
                Правила обновления и удаления
                
                1) Удаление
                
        RESTRICT - запрещает удаление строки из родительской таблицы, если 
        строка имеет потомков. Из родительской таблицы можно удалять только
        лишь те строки, которые не имеют потомков.
         
        CASCADE - при удаление родительской строки из родительской таблицы,
        все дочерние строки также удаляются из дочерней таблицы. 
        
        SET NULL - при удалении родительской строки из родительской таблицы
        внешним ключам во всех ее дочерних строках в дочерних таблицах 
        присваивается автоматически значение NULL. При удалении строки из родительской 
        таблицы вызывает установку значений NULL в некоторых столбцах дочерней таблицы.
        
        SET DEFAULT - при удалении родительской строки из родительской таблицы
        внешним ключам во всех ее дочерних строках присваивается определенное 
        значение, по умолчанию установленное для данного столбца.
        
        RESTRICT = NO ACTION
        
        ....CUSTOMERS (CUST_NUM) ON DELETE CASCADE,
        ... ON DELETE SET NULL,
        ... ON DELETE RESTRICT);
        
        
            2) UPDATE первичного ключа
        RESTRICT - запрещает обновление строки из родительской таблицы, если 
        строка имеет потомков. В родительской таблице можно обновлять первичные
        ключи только лишь тех строк, которые не имеют потомков.
         
        CASCADE - при изменении значения первичного ключа родительской строки
        из родительской таблицы, все дочерние строки также обновляются. 
        
        SET NULL - при обновлении первичного ключа родительской строки из родительской таблицы
        внешним ключам во всех ее дочерних строках в дочерних таблицах 
        присваивается автоматически значение NULL. При обновлении первичного ключа  строки из родительской 
        таблицы вызывает установку значений NULL в некоторых столбцах дочерней таблицы.
        
        SET DEFAULT - при обновлении первичного ключа родительской строки из родительской таблицы
        внешним ключам во всех ее дочерних строках присваивается определенное 
        значение, по умолчанию установленное для данного столбца.
        
        RESTRICT = NO ACTION
        
        ....CUSTOMERS (CUST_NUM) ON UPDATE CASCADE,
        ... ON UPDATE SET NULL,
        ... ON UPDATE RESTRICT);
        
        
        
            РЕЖИМЫ ВВОДА ДАННЫХ
        MATCH FULL - полное соответствие. Требует, чтобы внешние ключи таблицы-потомка
        были полностью равны первичному ключу таблицы-предка.В этом режиме ни одна часть 
        внешнего ключа не может содержать значение NULL, поэтому в правилах удаления и 
        обновления не затрагивается вопрос обработки этих значений.
         
        MATCH PARTIAL - частичное соответствие. Допускается что какая-то часть внешнего
        ключа имела значение NULL, при условии что остальная часть внешнего ключа равна
        соответствующей части какого-либо первичного ключа в таблице предке. Т.о. обработка
        значений NULL производится так, как было описано выше в правилах удалений и обновления       
"""

"""
        Утверждения
"""
# Гарантировать, что плановый объем продаж офиса не превысит сумму плановых объемов продаж его служащего
quiery_4 = f"CREATE ASSERTION target_valid" \
           f"   CHECK ((OFFICES.TARGET <= SUM(SALESREPS.QUOTA)) " \
           f"   AND" \
           f"          (SALESREPS.REP_OFFICE = OFFICES.OFFICE));"

quiery_5 = f"CREATE ASSERTION credit_orders" \
           f" CHECK (CUSTOMERS.CREDIT_LIMIT >= SELECT SUM(ORDERS>AMOUNT)" \
           f" FROM ORDERS WHERE ORDERS.CUST = CUSTOMERS.CUST_NUM);"

"""
                ТИПЫ ОГРАНИЧЕНИЙ
                
            NOT NULL - на уровне столбца. Запрещает присваивание ячейкам значений NULL.
            
            PRIMARY KEY - на уровне столбца или таблицы. Если первичный ключ состоит из
            одного столбца, данное ограничение на столбец. Если же на больше чем 1 столбец,
            то на таблицу.
             
            UNIQUE - на уровне столбца или таблицы. Если уникальным значение должно быть
            значение столбца, то ограничение на столбец. Если уникальным должно быть значение
            комбинации столбцов, то на таблицу.
             
            FOREIGN KEY - на уровне столбца или талицы. Если внешний ключ задается из одного 
            столбца, то на столбец. Если из комбинации столбцов то на таблицу.
            
            CHECK - на уровне столбца или таблицы. Единственное ограничение, которое может быть
            частью определения домена или утверждения.
"""

# Утверждение которое нам понадобится далее
quiery_6 = f"CREATE ASSERTION quota_totals" \
           f" CHECK ((OFFICES.TARGET = SUM(SALESREPS.QUOTA))" \
           f" AND (SALESREPS.REP_OFFICE = OFFICES.OFFICE));"
"""
    в утверждении выше говорится, что необходимо гарантировать, что плановый объем продаж будет
    всегда в точности равен сумме плановых объемов продаж его служащих.
    
    Данное утверждение неверно если не откладывать его до завершения транзакции.
    
            ПРОВЕРКА ОГРАНИЫЧЕНИЙ
            
        DEFERRABLE - проверка может быть отложена до окончания транзакции. Именно так должно
        быть определено утверждение выше. Для обновления плановых объемов продаж служащего
        или добавления информации о новых служащих нужно обязательно отложить проверку ограничений.
        
        NOT DEFERRABLE - не может быть отложена. Как правило относится к ограничениям на 
        первичный ключ и условия уникальности, а также на многие ограничения на значения столбцов.
        
        
            НАЧАЛЬНОЕ СОСТОЯНИЕ ОГРАНИЧЕНИЯ
            
        INITIALLY IMMEDIATE - ограничение начинает свою работу немедленно после
        выполнения каждой SQL инструкции.
         
        INITIALLY DEFERRED - проверяется по окончанию транзакции.  
"""

quiery_6_1 = f"CREATE ASSERTION quota_totals" \
            f" CHECK ((OFFICES.TARGET = SUM(SALESREPS.QUOTA))" \
            f" AND (SALESREPS.REP_OFFICE = OFFICES.OFFICE))" \
            f" DEFERRABLE INITIALLY IMMEDIATE;"
# Можно отложить, но в обычном режиме должно проверяться после каждой операции над БД.

# Для особой транзакции можно отложить проверку.
quiery_6_2 = f"SET CONSTRAINTS quota_totals DEFERRED" \
             f"" \
             f"INSERT INTO SALESREPS (EMPL_NUM, NAME, REP_OFFICE, HIRE_DATE, QUOTA, SALES)" \
             f" VALUES (:num, :name, :office_num, :date, :amount, 0);" \
             f"" \
             f"UPDATE OFFICES SET TARGET = TARGET + :amount" \
             f" WHERE (OFFICE = :office_num);" \
             f"" \
             f"COMMIT;"

"""
            ТРИГГЕРЫ
            
        С любым событием, вызывающим изменение содержимого таблицы,
        пользователь может связать действие (триггер), которое СУБД
        должна выполнять при каждом возникновении события.
"""

quiery_7 = f"CREATE TRIGGER (NEWORDER)" \
           f" ON ORDERS" \
           f" FOR INSERT" \
           f" AS UPDATE SALESREPS" \
           f"   SET SALES = SALES + INSERTED.AMOUNT" \
           f"   FROM SALESREPS, INSERTED" \
           f"   WHERE SALESREPS.EMPL_NUM = INSERTED.REP" \
           f"   UPDATE PRODUCTS" \
           f"   SET QTY_ON_HAND = QTY_ON_HAND - INSERTED.QTY" \
           f"   FROM PRODUCTS, INSERTED" \
           f"   WHERE PRODUCTS.MFR_ID = INSERTED.MFR" \
           f"   AND PRODUCTS.PRODUCT_ID = INSERTED.PRODUCT; "
"""
    quiery_7 говорит, что триггер вызывается каждый раз, когда к таблице 
    ORDERS обращается инструкция INSERT. В оставшейся части определения 
    (после слова AS) описывается действие, выполняемое триггером. В 
    данном случае это действие представляет собой последовательность двух
    инструкций UPDATE... Ссылка на добавляемую строку делается с помощью 
    имени псевдотаблицы INSERTED внутри инструкциий UPDATE.
    Кроме того,  могут присутствовать следующие инструкции: IF/ THEN/ ELSE,
    циклы, вызовы процедур и даже PRINT.  
"""

quiery_8 = f"CREATE TRIGGER REP_UPDATE" \
           f" ON SALESREPS" \
           f" FOR INSERT, UPDATE" \
           f" AS IF ((SELECT COUNT(*)" \
           f"           FROM OFFICES, INSERTED" \
           f"           WHERE OFFICES.OFFICE = INSERTED.REP_OFFICE) = 0)" \
           f"       BEGIN" \
           f"           PRINT('УКАЗАН неверный идентификатор офиса.'" \
           f"           ROLLBACK TRANSACTION" \
           f"       END;"

quiery_9 = f"CREATE TRIGGER CHANGE_REP_OFFICE" \
           f" ON OFFICES" \
           f" FOR UPDATE" \
           f" AS IF UPDATE (OFFICE)" \
           f"           BEGIN" \
           f"               UPDATE SALESREPS" \
           f"                   SET SALESREPS.REP_OFFICE = INSERTED.OFFICE" \
           f"                   FROM SALESREPS, INSERTED, DELETED" \
           f"                   WHERE SALESREPS.REP_OFFICE = DELETED.OFFICE" \
           f"            END;"

"""
            TRIGGER очень мощное правило
            которое не ограничивается парой строк.
            Может занимать сотни строчек кода для 
            обеспечения работы бизнес правил.
            
"""

# Делаем запрос к базе данных, используя обычный SQL-синтаксис
# cursor.execute(quiery_12)
cursor.execute(quiery_5)

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
