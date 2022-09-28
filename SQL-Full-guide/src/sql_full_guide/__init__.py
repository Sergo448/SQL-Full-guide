# -*- coding: utf-8 -*-
# Sergey.6362@mail.ru


import re
import sqlite3

# создаем подключение к нашей базе данных
conn = sqlite3.connect('./DATA_SQL/Database_book_A.sqlite')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ

""" First example """
# Делаем INSERT запрос к базе данных, используя обычный SQL-синтаксис
cursor.execute("SELECT NAME, HIRE_DATE FROM SALESREPS WHERE HIRE_DATE >= '05/30/2007' + 15")

# Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
# conn.commit()

results = cursor.fetchall()
print(results)

# Не забываем закрыть соединение с базой данных
conn.close()
