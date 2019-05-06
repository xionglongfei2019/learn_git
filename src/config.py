import pymysql
DEBUG = False
LOG_CONF = '../config/logging.conf'
DB=pymysql.connect("localhost", "mysqldb", "mysql", "mysqldb")