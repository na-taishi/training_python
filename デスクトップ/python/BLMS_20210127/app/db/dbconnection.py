import psycopg2
import config

#DB接続
def getConnection():
    users = config.db_conf.USERS
    dbnames = config.db_conf.DBNAMES
    passwords = config.db_conf.PASSWORD
    conn = psycopg2.connect(" user=" + users +" dbname=" + dbnames +" password=" + passwords)
    return conn

#comit
def commit(conn):
    conn.commit()

#close
def close(cur,conn):
    cur.close()
    conn.close()