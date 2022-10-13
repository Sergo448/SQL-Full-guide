import sqlite3

"""while True:
    conn = sqlite3.connect('./DATA_SQL/DATA_BOOK_A', timeout=1)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE CUSTOMERS SET CREDIT_LIMIT = 60000.00, CUST_REP = 109 WHERE COMPANY = 'Acme Mfg.';")
        result = cursor.fetchall()
        conn.commit()
    except sqlite3.OperationalError:
        print("database locked")
    num_users = len(result)
    conn.close()"""

conn = sqlite3.connect('./DATA_SQL/DATA_BOOK_A', timeout=1)
cursor = conn.cursor()


def _retry_if_exception(exception):
    return isinstance(exception, Exception)


@retry(retry_on_exception=_retry_if_exception,
       wait_random_min=1000,
       wait_random_max=5000,
       stop_max_attempt_number=5)
def execute(cmd, commit=True):
    conn.execute(cmd)
    conn.commit()


execute("UPDATE CUSTOMERS SET CREDIT_LIMIT = 60000.00, CUST_REP = 109 WHERE COMPANY = 'Acme Mfg.';")
conn.close()
