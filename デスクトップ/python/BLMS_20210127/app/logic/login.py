import db

#ログイン画面、ユーザー登録画面処理

#DB接続
def connect_db():
    return db.dbconnection.getConnection()

#DBcommit
def commit(conn):
    db.dbconnection.commit(conn)

#DBclose
def close(cur,conn):
    db.dbconnection.close(cur,conn)

#ログイン確認
def check_user(employee_number,passowrod):
    conn = connect_db()
    cur = conn.cursor()
    sql = db.users_sql.check_user
    values = (employee_number,passowrod)
    cur.execute(sql,values)
    result = cur.fetchone()
    close(cur,conn)
    return result

#ユーザー登録
def register_user(employee_number,name,division,mail_address,password):
    conn = connect_db()
    cur = conn.cursor()
    flg = 0
    #既存ユーザー確認
    sql1 = db.users_sql.find_user
    cur.execute(sql1,(employee_number,))
    result = cur.fetchone()
    if not result:
        #社員番号が重複しなければ登録
        sql2 = db.users_sql.register_user
        values = (employee_number,name,division,mail_address,password)
        cur.execute(sql2,values)
    else:
        flg = 1

    commit(conn)
    close(cur,conn)
    return flg
