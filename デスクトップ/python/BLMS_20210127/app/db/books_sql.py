#書籍取得(単体)
find_book = "SELECT * FROM books WHERE id = %s;"

# #書籍全取得→現在未使用
# find_book_list = "SELECT * FROM books;"

#書籍全取得(現在借りている書籍除外)
find_book_list = "SELECT * FROM books WHERE id not in(SELECT book_id FROM lending_status WHERE borrower = %s AND return_status = 0);"

#書籍取得(あいまい検索)
search_title = "SELECT * FROM books WHERE title like %s AND id not in(SELECT book_id FROM lending_status WHERE borrower = %s AND return_status = 0);"
search_author = "SELECT * FROM books WHERE author like %s AND id not in(SELECT book_id FROM lending_status WHERE borrower = %s AND return_status = 0);"
search_publisher = "SELECT * FROM books WHERE publisher like %s AND id not in(SELECT book_id FROM lending_status WHERE borrower = %s AND return_status = 0);"

#在庫数更新
update_stock = "UPDATE books SET (stock,updated_at) = (stock+%s,%s) WHERE id = %s;"

#書籍登録
add_book = "INSERT INTO books (title,author,publisher,price,buyer,purchase_date,total,stock,genre) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"

#書籍削除
delete_book = "DELETE FROM books WHERE id = %s;"

#書籍更新
update_book = "UPDATE books SET (title,author,publisher,price,buyer,purchase_date,total,stock,updated_at,genre) = (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) WHERE id = %s;"
