import db
import logic
import numpy as np

#テストデータ作成用

#DB接続
def connect_db():
    return db.dbconnection.getConnection()

#DBclose
def close(cur,conn):
    db.dbconnection.close(cur,conn)

#借用テストデータ作成
def test_borrowed(borrower,expected_return_date,stock,book_id,checkout_date):
    
    conn = connect_db()
    cur = conn.cursor()
    #lending_statusテーブルに追加
    sql1 = "INSERT INTO lending_status (book_id,borrower,expected_return_date,checkout_date) VALUES(%s,%s,%s,%s);"
    cur.execute(sql1,(book_id,borrower,expected_return_date,checkout_date))
    
    #lending_statusに登録したidの在庫数、更新日を更新(在庫数は借りる数引く)
    updated_at = logic.datetime_format.get_current_time()
    sql2 = "UPDATE books SET (stock,updated_at) = (stock+%s,%s) WHERE id = %s;"
    cur.execute(sql2,(-stock,updated_at,book_id))

    close(cur,conn)

#テストユーザー作成
def test_create_user(employee_number,name,division,mail_address,password,status):
    conn = connect_db()
    cur = conn.cursor()
    sql = "INSERT INTO users (employee_number,name,division,mail_address,password,status) VALUES(%s,%s,%s,%s,%s,%s);"
    cur.execute(sql,(employee_number,name,division,mail_address,password,status))
    close(cur,conn)

#現在存在書籍のidを取得
def get_books_id():
    conn = connect_db()
    cur = conn.cursor()
    sql = "SELECT id FROM books;"
    cur.execute(sql)
    tmp_result = cur.fetchall()
    close(cur,conn)
    result = []

    for i in tmp_result:
        result.append(i[0])

    return result

#日付の生成
def random_date_generator(start_date, range_in_days):
    days_to_add = np.arange(0, range_in_days)
    random_date = np.datetime64(start_date) + np.random.choice(days_to_add)
    return random_date
