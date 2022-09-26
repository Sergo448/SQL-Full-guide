# db -> './DATA_SQL/Database_book_A.sqbpro'
# Sergo448
# Sergey.6362@mail.ru
import re
# imports
import sqlite3

# connecting to the database
db = sqlite3.connect('./DATA_SQL/Database_book_A.sqbpro')

# Quiery
stmt = "SELECT NAME, HIRE_DATE" + '\n' + \
       "FROM SALESREPS" + '\n' + \
       "WHERE HIRE_DATE >= '05/30/2007' + 15 DAYS;"

stmt = re.sub('\s+', ' ', stmt.replace('\n', ' ').replace('\r', ''))
print(db.cursor(stmt))
print(db.execute(stmt))
