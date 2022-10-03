# -*- coding: utf-8 -*-
# Sergey.6362@mail.ru


import sqlite3

quiery = """
            CREATE TABLE PRODUCTS
            (MFR_ID CHAR(3) NOT NULL,
            PRODUCT_ID CHAR(5) NOT NULL,
            DESCRIPTION VARCHAR(20) NOT NULL,
            PRICE DECIMAL(9,2) NOT NULL,
            QTY_ON_HAND INTEGER NOT NULL,
            primary key (MFR_ID, PRODUCT_ID));
            
            CREATE TABLE SALESREPS
            (EMPL_NUM INTEGER NOT NULL,
            NAME VARCHAR (15) NOT NULL,
            AGE INTEGER,
            REP_OFFICE integer,
            TITLE VARCHAR(10),
            HIRE_DATE DATE NOT NULL,
            MANAGER integer,
            QUOTA DECIMAL (9,2),
            SALES DECIMAL (9,2) NOT NULL,
            PRIMARY KEY (EMPL_NUM),
            FOREIGN KEY (MANAGER)
            REFERENCES SALESREPS
            ON DELETE SET NULL,
            CONSTRAINT WORKSIN FOREIGN KEY (REP_OFFICE) REFERENCES OFFICES(OFFICE)
            ON delete SET NULL);
            
            CREATE TABLE OFFICES
            (OFFICE INTEGER NOT NULL,
            CITY VARCHAR(15) NOT NULL,
            REGION VARCHAR(10) NOT NULL,
            MGR INTEGER, TARGET DECIMAL(9,2),
            SALES DECIMAL(9,2) NOT NULL,
            PRIMARY KEY (OFFICE),
            CONSTRAINT HASMGR FOREIGN KEY (MGR) REFERENCES SALESREPS(EMPL_NUM)
            ON DELETE SET NULL);
            
            CREATE TABLE CUSTOMERS
            (CUST_NUM INTEGER NOT NULL,
            COMPANY VARCHAR (20) NOT NULL,
            CUST_REP INTEGER,
            CREDIT_LIMIT DECIMAL(9,2),
            PRIMARY KEY (CUST_NUM),
            CONSTRAINT HASREP FOREIGN KEY (CUST_REP) REFERENCES SALESREPS(EMPL_NUM)
            ON DELETE SET NULL);
            
            CREATE TABLE ORDERS
            (ORDER_NUM INTEGER NOT NULL,
            ORDER_DATE DATE NOT NULL,
            CUST INTEGER NOT NULL,
            REP INTEGER,
            MFR CHAR(3) NOT NULL,
            PRODUCT CHAR(5) NOT NULL,
            QTY INTEGER NOT NULL,
            AMOUNT DECIMAL (9,2) NOT NULL,
            primary key (ORDER_NUM),
            CONSTRAINT PLACEDBY FOREIGN KEY (CUST) REFERENCES CUSTOMERS(CUST_NUM)
            ON DELETE CASCADE,
            CONSTRAINT TAKENBY FOREIGN KEY (REP) REFERENCES SALESREPS(EMPL_NUM)
            ON DELETE SET NULL,
            CONSTRAINT ISFOR FOREIGN KEY (MFR, PRODUCT) REFERENCES PRODUCTS(MFR_ID, PRODUCT_ID)
            ON DELETE RESTRICT);
            
            
            -- ALTER TABLE OFFICES
            -- ADD CONSTRAINT HASMGR FOREIGN KEY(MGR) REFERENCES SALESREPS (EMPL_NUM) ON DELETE SET NULL;
            -- ALTER TABLE SALESREPS
            -- ADD CONSTRAINT WORKSIN FOREIGN KEY(REP_OFFICE) REFERENCES OFFICES (OFFICE) ON DELETE SET NULL;
"""


# Тут дальше должен быть код использующий функционал питона для
# реализации SQL запросов, но его не будет, т.к. база данных
# была полностью сделана в DB SQLite browser