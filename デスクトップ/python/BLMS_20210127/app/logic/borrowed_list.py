import db
import logic
import datetime

#借用書籍一覧画面処理

#DB接続
def connect_db():
    return db.dbconnection.getConnection()

#DBcommit
def commit(conn):
    db.dbconnection.commit(conn)

#DBclose
def close(cur,conn):
    db.dbconnection.close(cur,conn)

#借用書籍取得
def get_borrower_list(borrower):
    conn = connect_db()
    cur = conn.cursor()
    sql = db.lending_status_sql.find_borrowed_list
    cur.execute(sql,(borrower,))
    result = cur.fetchall()

    count = 0
    for i in result:
        i = logic.datetime_format.change_tuple(i,6)
        result[count] = i
        count += 1

    close(cur,conn)
    return result

#返却処理
def return_borrowed(book_id,borrower,stock):
    conn = connect_db()
    cur = conn.cursor()
    #lending_statusテーブルのreturn_statusを1に変更
    return_date = logic.datetime_format.get_current_time()
    return_status = 1
    sql1 = db.lending_status_sql.update_return_status
    cur.execute(sql1,(return_date,return_status,book_id,borrower))
    
    #在庫数を変更
    updated_at = logic.datetime_format.get_current_time()
    sql2 = db.books_sql.update_stock
    cur.execute(sql2,(stock,updated_at,book_id))
    
    commit(conn)
    close(cur,conn)
