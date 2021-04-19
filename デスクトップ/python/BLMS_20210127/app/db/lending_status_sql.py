
#ログインユーザーの借用書籍を取得(書籍一覧除外用)→現在未使用
find_borrowed = "SELECT book_id FROM lending_status WHERE borrower = %s AND return_status = 0;"

#対象書籍の直近の返却予定日
find_return_date = "SELECT expected_return_date FROM lending_status WHERE book_id = %s AND return_status = 0 ORDER BY expected_return_date LIMIT 1;"

#登録処理
add_lending_status = "INSERT INTO lending_status (book_id,borrower,expected_return_date) VALUES(%s,%s,%s);"

#ステータス変更
update_return_status = "UPDATE lending_status  SET (return_date,return_status) = (%s,%s) WHERE book_id = %s AND borrower = %s;"

#ログインユーザーの借用書籍を取得(booksテーブルとlending_statusテーブルを結合して、書籍情報を取得)
find_borrowed_list = '''
SELECT
    book_id,
    borrower,
    title,
    author,
    publisher,
    checkout_date,
    expected_return_date
FROM
    lending_status as ls
    INNER JOIN
        books
    ON  ls.book_id = books.id
WHERE
    ls.borrower = %s
AND ls.return_status = 0'''

#ジャンル別カウント
count_genre_all = '''
SELECT
    lb.genre,
    COUNT(lb.genre)
FROM
    (
        SELECT
            ls.book_id,
            books.genre,
            ls.return_status,
            ls.checkout_date,
            ls.return_date
        FROM
            lending_status as ls
            INNER JOIN
                books
            ON  ls.book_id = books.id
    ) as lb
GROUP BY
    lb.genre
ORDER BY
    COUNT(lb.genre) DESC
LIMIT 5
;'''

#ジャンル別カウント(月間)
count_genre_month = '''
SELECT
    lb.genre,
    COUNT(lb.genre)
FROM
    (
        SELECT
            ls.book_id,
            books.genre,
            ls.return_status,
            ls.checkout_date,
            ls.return_date
        FROM
            lending_status as ls
            INNER JOIN
                books
            ON  ls.book_id = books.id
    ) as lb
WHERE
    DATE_PART('year', NOW()) = DATE_PART('year', checkout_date)
AND DATE_PART('month', NOW()) = DATE_PART('month', checkout_date)
GROUP BY
    lb.genre
ORDER BY
    COUNT(lb.genre) DESC
LIMIT 5
;'''

#ジャンル別カウント(年間)
count_genre_year = '''
SELECT
    lb.genre,
    COUNT(lb.genre)
FROM
    (
        SELECT
            ls.book_id,
            books.genre,
            ls.return_status,
            ls.checkout_date,
            ls.return_date
        FROM
            lending_status as ls
            INNER JOIN
                books
            ON  ls.book_id = books.id
    ) as lb
WHERE
    checkout_date >=(SELECT DATE_TRUNC('month', now()) + '-1 years')
GROUP BY
    lb.genre
ORDER BY
    COUNT(lb.genre) DESC
LIMIT 5
;'''

#貸出数(月間)未使用
count_checkout = '''
SELECT
    DATE_TRUNC('MONTH', ls.checkout_date) as month,
    books.genre,
    COUNT(ls.checkout_date)
FROM
    lending_status as ls
    INNER JOIN
        books
    ON  ls.book_id = books.id
GROUP BY
    books.genre,
    month
ORDER BY
    month,
    books.genre
;'''

#各ジャンルの月毎の貸出数(年間)
borrowing_number_genre ='''
SELECT
    %s as checkout_date,
    %s as genre,
    COUNT(lb.genre)
FROM
    (
        SELECT
            ls.book_id,
            books.genre,
            ls.checkout_date
        FROM
            lending_status as ls
            INNER JOIN
                books
            ON  ls.book_id = books.id
    ) as lb
WHERE
    CAST(checkout_date AS VARCHAR) like %s
AND genre = %s
;'''

#指定した年の貸出状況を取得
get_specified_year ='''
SELECT
    ls.book_id,
    books.genre,
    ls.checkout_date
FROM
    lending_status as ls
    INNER JOIN
        books
    ON  ls.book_id = books.id
WHERE
    CAST(checkout_date AS VARCHAR) like %s
;'''

#1年以上借りられていない書籍(1年間以上の購入日の経過かつ借用されていない書籍)
not_borrowed = '''
SELECT
    id,
    title,
    genre,
    total,
    purchase_date
FROM
    books
WHERE
    id NOT IN(
        SELECT
            book_id as id
        FROM
            lending_status
        WHERE
            checkout_date >= (
                SELECT
                    DATE_TRUNC('month', now()) + '-1 years'
            )
        GROUP BY
            book_id
    )
AND purchase_date <= (
        SELECT
            DATE_TRUNC('month', now()) + '-1 years'
    )
;'''
