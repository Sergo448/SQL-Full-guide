# -*- coding: utf-8 -*-
# Sergey.6362@mail.ru


import re
import sqlite3

# создаем подключение к нашей базе данных
conn = sqlite3.connect('./DATA_SQL/DATA_BOOK_A')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ
quiery_1 = """
SELECT NAME, HIRE_DATE 
FROM SALESREPS
WHERE HIRE_DATE >= '05/30/2007' + 15 DAYS;
"""

quiery_1_1 = """
SELECT NAME, HIRE_DATE 
FROM SALESREPS
WHERE HIRE_DATE >= '05/30/2007';
"""

# Делаем запрос к базе данных, используя обычный SQL-синтаксис
cursor.executescript(quiery_1_1)

# Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
# conn.commit()

results = cursor.fetchall()
print(results)

# Не забываем закрыть соединение с базой данных
conn.close()
