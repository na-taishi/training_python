import db
import logic
import numpy as np
import pandas as pd

#分析用処理

#DB接続
def connect_db():
    return db.dbconnection.getConnection()

#DBclose
def close(cur,conn):
    db.dbconnection.close(cur,conn)

#ジャンルの種類を取得
def get_genre_type(result,cl_num):
    rows = np.array(result)
    num = rows.shape[0]
    genre_list = np.empty(num,dtype=object)
    for count,row in enumerate(rows):
        genre_list[count] =row[cl_num]
    return np.unique(genre_list)

#ジャンル別カウントのグラフ作成
def get_genre(period):
    #DBからデータ取得
    conn = connect_db()
    cur = conn.cursor()
    if period == "all":
        sql = db.lending_status_sql.count_genre_all
        title = "貸出総数(ジャンル別)"
    elif period == "month":
        sql = db.lending_status_sql.count_genre_month
        title = "今月の貸出数(ジャンル別)"
    elif period == "year":
        sql = db.lending_status_sql.count_genre_year
        title = "今日から1年前までの貸出数(ジャンル別)"
    cur.execute(sql)
    result = cur.fetchall()
    close(cur,conn)

    #グラフ作成
    if not result:
        data = False
    else:
        data = logic.create_graph.make_bar(result,title)
    return data

#長期間の貸し出しがない書籍
def not_borrow_long_period():
    #DBからデータ取得
    conn = connect_db()
    df = pd.read_sql(db.lending_status_sql.not_borrowed,conn)
    cur = conn.cursor()
    close(cur,conn)
    
    #ジャンルの種類を取得
    genre_list = df["genre"].unique()

    if genre_list.size == 0:
        data = False
    else:
        title = "1年以上貸し出しがない書籍"
        data = logic.create_graph.make_scatter(df,genre_list,title)
    return data

#ジャンル別各月総数
def create_monthly_genre_count(specified_year):
    #ジャンルの種類を取得
    conn = connect_db()
    cur = conn.cursor()
    sql1 = db.lending_status_sql.get_specified_year
    cur.execute(sql1,(specified_year+'%',))
    result1 = cur.fetchall()
    genre_list = get_genre_type(result1,1)
    if genre_list.size == 0:
        #genre_listが空の場合、グラフ作成するためのデータがないと判定し、Falseを返す
        data = False
    else:
        #1年間のデータをジャンル毎に取得
        sql2 = db.lending_status_sql.borrowing_number_genre
        result2 = np.empty(len(genre_list),dtype=object)
        for count,genre in enumerate(genre_list):
            month_list = np.empty(12,dtype=object)
            for i in range(1,13):
                if i < 10:
                    month = specified_year + "-0" +str(i)
                else:
                    month = specified_year +"-"+str(i)
                values = (month,genre,month+'%',genre)
                cur.execute(sql2,values)
                month_list[i-1] = cur.fetchone()
            result2[count] = month_list
    
        #グラフ作成
        title = specified_year + "年の月別貸出数(ジャンル別)"
        data = logic.create_graph.make_plot(result2,genre_list,title)
    
    close(cur,conn)
    
    return data
