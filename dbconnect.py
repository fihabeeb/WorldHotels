# - 22066955 Fadil Idris
import mysql.connector
from mysql.connector import errorcode

# MYSQL CONFIG VARIABLES
hostname  = "127.0.0.1"
username    = "root"
passwd  = "2005iscool"
db = "World_Hotels"
def getConnection():
    try:
        conn = mysql.connector.connect(host=hostname,
                                        user=username,
                                        password=passwd,
                                        database=db)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)
    else:  #will execute if there is no exception raised in try block
        return conn
