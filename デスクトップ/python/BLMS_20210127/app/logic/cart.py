import db
import logic
import datetime

#カート画面処理

#DB接続
def connect_db():
    return db.dbconnection.getConnection()

#DBcommit
def commit(conn):
    db.dbconnection.commit(conn)

#DBclose
def close(cur,conn):
    db.dbconnection.close(cur,conn)


#書籍取得
def get_book_cart(books):
    conn = connect_db()
    cur = conn.cursor()
    #セッションに保存した書籍IDリストの書籍を取得
    sql = db.books_sql.find_book
    result = ()
    if books:
        #setで重複を除外
        books = set(books)
        for book in books:
            cur.execute(sql,(book,))
            result = result + (cur.fetchone(),)
    
    close(cur,conn)
    return result
    

#借用処理
def borrow(borrower,expected_return_date,stock,book_id):
    conn = connect_db()
    cur = conn.cursor()
    #lending_statusテーブルに追加
    sql1 = db.lending_status_sql.add_lending_status
    cur.execute(sql1,(book_id,borrower,expected_return_date))
    
    #lending_statusに登録したidの在庫数、更新日を更新(在庫数は借りる数引く)
    updated_at = logic.datetime_format.get_current_time()
    sql2 = db.books_sql.update_stock
    cur.execute(sql2,(-stock,updated_at,book_id))
    
    commit(conn)
    close(cur,conn)