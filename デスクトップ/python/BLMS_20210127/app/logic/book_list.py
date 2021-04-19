import db

#書籍一覧画面、書籍登録画面処理

#DB接続
def connect_db():
    return db.dbconnection.getConnection()

#DBcommit
def commit(conn):
    db.dbconnection.commit(conn)

#DBclose
def close(cur,conn):
    db.dbconnection.close(cur,conn)

#書籍一覧取得
def get_book_list(borrower):
    conn = connect_db()
    cur = conn.cursor()
    sql = db.books_sql.find_book_list
    cur.execute(sql,(borrower,))
    result = cur.fetchall()
    close(cur,conn)
    return result

#書籍検索
def get_books_search(search,selection,borrower):
    conn = connect_db()
    cur = conn.cursor()
    if selection == "タイトル":
        sql = db.books_sql.search_title
    elif selection == "著者":
        sql = db.books_sql.search_author
    elif selection == "出版社":
        sql = db.books_sql.search_publisher
    cur.execute(sql,(search+"%",borrower))
    
    result = cur.fetchall()
    close(cur,conn)
    return result

#書籍登録
def register_book(title,author,publisher,price,buyer,purchase_date,total,genre):
    conn = connect_db()
    cur = conn.cursor()
    sql = db.books_sql.add_book
    if not price:
        price = None
    #書籍を新規に登録するため、在庫数は総数と同じになる
    stock = total
    values = [title,author,publisher,price,buyer,purchase_date,total,stock,genre]
    cur.execute(sql,values)
    commit(conn)
    close(cur,conn)

 #チェックボックスの非活性化
def change_disabled(result,books):
    rows = list(result)
    count = 0
    for row in rows:
        disabled = ""
        #在庫がない書籍の非活性化
        if row[8] <= 0:
            disabled = "disabled"
        elif books:
            #カートにある書籍を非活性
            if str(row[0]) in books:
                disabled = "disabled"
        row = row + (disabled,)
        rows[count] = row
        count += 1
    result = tuple(rows)
    return result