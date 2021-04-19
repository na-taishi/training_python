import db
import datetime

#管理者画面処理

#DB接続
def connect_db():
    return db.dbconnection.getConnection()

#DBcommit
def commit(conn):
    db.dbconnection.commit(conn)

#DBclose
def close(cur,conn):
    db.dbconnection.close(cur,conn)

#ユーザ一覧取得
def get_user_list():
    conn = connect_db()
    cur = conn.cursor()
    sql = db.users_sql.find_user_all
    cur.execute(sql)
    result = cur.fetchall()
    close(cur,conn)
    return result

#ユーザ一検索
def get_users_search(search,selection):
    conn = connect_db()
    cur = conn.cursor()
    if selection == "社員番号":
        sql = db.users_sql.search_number
    elif selection == "社員名":
        sql = db.users_sql.search_name
    elif selection == "事業部":
        sql = db.users_sql.search_division
    
    if selection == "使用可能":
        sql = db.users_sql.available_users
        cur.execute(sql)
    elif selection == "使用不能":
        sql = db.users_sql.unusable_users
        cur.execute(sql)
    else:
        cur.execute(sql,(search+"%",))  
    result = cur.fetchall()
    close(cur,conn)
    return result

#ステータス変更
def update_status(employee_number,status):
    conn = connect_db()
    cur = conn.cursor()
    sql = db.users_sql.update_status
    updated_at = datetime.datetime.now()
    if status == "0":
        status = "1"
    elif status == "1":
        status = "0"
    values = (updated_at,status,employee_number)
    cur.execute(sql,values)
    commit(conn)
    close(cur,conn)

#ユーザー情報変更
def update_user(employee_number,name,division,mail_address,password,status):
    conn = connect_db()
    cur = conn.cursor()
    sql = db.users_sql.update_user
    updated_at = datetime.datetime.now()
    values = (employee_number,name,division,mail_address,password,updated_at,status,employee_number)
    cur.execute(sql,values)
    commit(conn)
    close(cur,conn)

#ユーザー削除
def delete_user(employee_number):
    conn = connect_db()
    cur = conn.cursor()
    sql = db.users_sql.delete_user
    cur.execute(sql,(employee_number,))
    commit(conn)
    close(cur,conn)