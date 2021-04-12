import traceback
import glob

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

import config
import common
from common import dbconnection as db

#テーブルデータ取得
def get_table(sql):
    conn = db.getConnection()
    df = pd.read_sql(sql,con = conn)
    cur = conn.cursor()
    db.close(cur,conn)
    return df

#テーブルデータ取得(パラメータあり)
def get_table_par(sql,par):
    conn = db.getConnection()
    df = pd.read_sql(sql,con = conn,params =par)
    cur = conn.cursor()
    db.close(cur,conn)
    return df

#ファイルのシート名を全て取得
def get_sheet_names(path):
     #ブックを取得
    df = pd.ExcelFile(path)
     #シートを取得 
    sheets = df.sheet_names
    return sheets

#全シート、シート名取得
def get_excel(path):
    #ブックを取得
    ob = pd.ExcelFile(path)
    #データフレームとシート名をリストに入れる
    sheets = ob.sheet_names
    df_list = ob.parse(sheets)
    excel_data =[df_list,sheets]
    return excel_data

#テーブル作成(テーブル名が重複する場合は書き換える)
def export_table(df,tbl_name):
    flg = True
    try:
        engine=create_engine("postgresql://" +config.db_conf.USERS+":"+config.db_conf.PASSWORD+"@"+"/"+config.db_conf.DBNAMES)
        df.to_sql(tbl_name,engine,if_exists="replace",index=False)
    except Exception as e:
        flg = False
        print("DB_ERROR",end=":")
        print(e)
        print(traceback.format_exc())
    return flg

#データフレームを縦に結合
def concat_df(df_list):
    df = pd.concat(df_list,ignore_index=True)
    return df


#データフレームを横に結合
def join_df(df_list,left_list,right_list):
    df = df_list[0]
    df_list.pop(0)
    for count,tmp_df in enumerate(df_list):
        df = pd.merge(df,tmp_df,left_on=left_list[count], right_on=right_list[count],suffixes=['', '_right'])
    return df

#データフレームを横に結合(left_join)
def left_join_df(df_list,left_list,right_list):
    df = df_list[0]
    df_list.pop(0)
    for count,tmp_df in enumerate(df_list):
        df = pd.merge(df,tmp_df,left_on=left_list[count], right_on=right_list[count],suffixes=['', '_right'],how='left')
    return df

#データフレームを種類別に格納
def create_df_list(df,values,col_name):
    df_list = []
    for value in values:
        df_loc = df.loc[df[col_name]==value]
        df_list.append(df_loc)
    return df_list

#ディレクトリにある指定した拡張子のファイルすべて取得(header変数はヘッダーなしならNone)
def read_dir(dir_path,extension,header):
    df_list = []
    if extension == "csv":
        paths = glob.glob(dir_path + "*.csv")
        for path in paths:
            df = pd.read_csv(path,encoding='cp932',header=header)
            # df = pd.read_csv(path,encoding='utf-8',header=header)
            df_list.append(df)
    elif extension == "xlsx":
        paths = glob.glob(dir_path + "*.xlsx")
        for path in paths:
            df = pd.read_excel(path)
            df_list.append(df)
    return df_list
