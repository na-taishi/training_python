import db
import logic
import datetime

#詳細画面処理

#DB接続
def connect_db():
    return db.dbconnection.getConnection()

#DBcommit
def commit(conn):
    db.dbconnection.commit(conn)

#DBclose
def close(cur,conn):
    db.dbconnection.close(cur,conn)

#戻るボタンの遷移先
def return_screen(title):
    if title =="書籍一覧":
        screen = "/book_list"
    elif title =="借用一覧":
        screen = "/borrowed_list"
    elif title =="カート":
        screen = "/cart"

    return screen

#カート追加ボタンの非活性化
def change_disabled(title,stock,books,book_id):
    disabled =None
    if title =="書籍一覧":
        if stock <= 0:
            disabled = "disabled"
        elif books:
            if book_id in books:
                disabled = "disabled"
        else:
            disabled = ""
    elif title =="借用一覧":
        disabled = "disabled"
    elif title =="カート":
        disabled = "disabled"

    return disabled

#書籍詳細取得
def get_book_detail(book_id):
    conn = connect_db()
    cur = conn.cursor()
    #書籍詳細取得
    sql1 = db.books_sql.find_book
    cur.execute(sql1,(book_id,))
    result = cur.fetchone()
    #返却予定日取得
    sql2 = db.lending_status_sql.find_return_date
    cur.execute(sql2,(book_id,))
    result2 = cur.fetchone()

    #購入日と返却日のフォーマットの変更
    result = logic.datetime_format.change_tuple(result,6)
    return_date = logic.datetime_format.change_tuple(result2,0)

    if return_date:
        result = result + (return_date[0],)

    close(cur,conn)
    return result

#書籍更新
def update_book(book_id,title,author,publisher,price,buyer,purchase_date,total,genre):
    conn = connect_db()
    cur = conn.cursor()
    #在庫数の計算
    sql1 = db.books_sql.find_book
    cur.execute(sql1,(book_id,))
    tmp = cur.fetchone()
    difference = int(total) - tmp[7]
    now_stock = tmp[8]
    stock = now_stock + difference

    #更新
    sql2 = db.books_sql.update_book
    updated_at = logic.datetime_format.get_current_time()
    values = [title,author,publisher,price,buyer,purchase_date,total,stock,updated_at,genre,book_id]
    cur.execute(sql2,values)    

    commit(conn)
    close(cur,conn)

#書籍削除
def delete_book(book_id):
    conn = connect_db()
    cur = conn.cursor()
    sql = db.books_sql.delete_book
    cur.execute(sql,(book_id,))
    commit(conn) 
    close(cur,conn)
