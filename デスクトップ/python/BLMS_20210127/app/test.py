import db
import logic
import datetime
import make_test_data
import random
import pandas as pd
import numpy as np
import traceback
import config

###--------テストデータ作成------------
#ユーザー作成
# employee_number=7
# name="更新アカウント_2"
# division="更新"
# mail_address="update_test_2"+"@test.jp"
# password=12345678
# status=0
# make_test_data.test_create_user(employee_number,name,division,mail_address,password,status)

#書籍登録
# title="テスト＿2年前の実用書_1"
# author="テスト2年前_実用書_1"
# publisher="テストB社"
# price=1000
# buyer="テスト＿太郎"
# purchase_date="20190301"
# total=2
# genre="実用書"
# logic.book_list.register_book(title, author, publisher, price, buyer, purchase_date, total, genre)

#書籍登録(大量登録)
# num = 510
# title_list =["テスト＿実用書","テスト＿プログラミング","テスト＿資格","テスト＿参考書","テスト＿料理"]
# author_list=["テスト＿太郎","テスト＿次郎","テスト＿三郎","テスト＿四郎","テスト＿五郎"]
# publisher_list=["テスト＿A社","テスト＿B社","テスト＿C社","テスト＿D社","テスト＿E社"]
# price_list=[100,1000,1700,2800,5000]
# buyer_list=["田中　太郎","佐藤　次郎","山田　三郎"]
# purchase_date_start=["2018-01-01",760]
# genre_list=["実用書","プログラミング","資格","参考書","料理"]
# genre_number = 4
# for i in range(num):
#     title = title_list[genre_number] + str(i)
#     author = author_list[random.randint(0,4)]
#     publisher = random.choice(publisher_list)
#     price = random.choice(price_list)
#     buyer = random.choice(buyer_list)
#     purchase_date=str(make_test_data.random_date_generator(purchase_date_start[0],purchase_date_start[1]))
#     total=random.randint(1,10)
#     genre = genre_list[genre_number]
#     logic.book_list.register_book(title, author, publisher, price, buyer, purchase_date, total, genre)


# #借用(stockは基本的に「1」(借りる数のため))
# borrower=1005
# expected_return_date="20201010"
# stock=1
# book_id=9
# checkout_date="20171201"
# make_test_data.test_borrowed(borrower,expected_return_date,stock,book_id,checkout_date)

# #返却(stockは基本的に「1」(返却数のため))
# book_id=15
# borrower=1005
# stock=1
# logic.borrowed_list.return_borrowed(book_id,borrower,stock)

# #借用と返却
# num = 100
# borrower_list=[1010,1011,1012,1013,1014,1015,1016,1017,1018,1019]
# checkout_date_list=["2020-01-01",360]
# stock=1
# book_id_list= make_test_data.get_books_id()
# expected_return_date_list=["2020-01-01",360]
# for i in range(num):
#     borrower=random.choice(borrower_list)
#     checkout_date=str(make_test_data.random_date_generator(checkout_date_list[0],checkout_date_list[1]))
#     expected_return_date=str(make_test_data.random_date_generator(expected_return_date_list[0],expected_return_date_list[1]))
#     book_id=random.choice(book_id_list)
#     make_test_data.test_borrowed(borrower,expected_return_date,stock,book_id,checkout_date)
#     logic.borrowed_list.return_borrowed(book_id,borrower,stock)

###------------------------------------
