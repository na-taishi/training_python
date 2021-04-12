import numpy as np
import pandas as pd

import config
import common
from config import file_conf as file
from common import pandas_data as com_pd

##1人当たり##

sql1 =common.db_sql.sql_dict["1回あたりの旅行単価"]
sql2 =common.db_sql.sql_dict["1人当たりの日帰り旅行回数"]
sql3 =common.db_sql.sql_dict["1人当たりの宿泊旅行回数"]
sql4 =common.db_sql.sql_dict["1人当たりの宿泊数"]

#データフレームの作成
def create_join_df(sql_list,left_list,right_list):
	df_list =[]
	for i,sql in enumerate(sql_list):
		df = com_pd.get_table(sql)
		df_list.append(df)
	df = com_pd.join_df(df_list,left_list,right_list)
	return df

#結合キーが1種類の時のデータフレーム作成
def condition_one_df(sql_list,col_name):
	num = len(sql_list) - 1
	left_list = [col_name] * num
	right_list = [col_name] * num
	df = create_join_df(sql_list,left_list,right_list)
	return df

#種類で分別する
def sort_category(sql_list,category):
	col_name = '年'
	df = condition_one_df(sql_list,col_name)
	df_loc = df.loc[df['種類']==category]
	return df_loc


#日帰り旅行の単価と回数
def day_trip():
	#データフレーム作成
	sql_list = [sql1,sql2]
	category = "日帰り"
	df = sort_category(sql_list, category)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":日帰り旅行の単価と回数"
	x = '年'
	y1 = '単価'
	y2 = '回数'
	df_list = [df]
	legend_list1 = ["単価"]
	legend_list2 = ["回数"]
	times_min =df['回数'].min()
	times_max =df['回数'].max()
	axis = [None,"単価","回数"]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	png_path = file.png_export_path("day_trip")
	excel_path = file.excel_export_path("day_trip")
	col_del = []
	sheet_name='日帰り旅行の単価と回数'
	position = "B" + str(len(df) + 5)
	index_flg = False
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df)
	return flg

#宿泊旅行の単価と回数
def staying_trip_price_times():
	#データフレーム作成
	sql_list = [sql1,sql3]
	category = "宿泊旅行"
	df = sort_category(sql_list, category)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":宿泊旅行の単価と回数"
	x = '年'
	y1 = '単価'
	y2 = '回数'
	df_list = [df]
	legend_list1 = ["単価"]
	legend_list2 = ["回数"]
	times_min =df['回数'].min()
	times_max =df['回数'].max()
	axis = [None,"単価","回数"]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	png_path = file.png_export_path("staying_trip_price_times")
	excel_path = file.excel_export_path("staying_trip_price_times")
	col_del = []
	sheet_name='宿泊旅行の単価と回数'
	position = "B" + str(len(df) + 5)
	index_flg = False
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df)
	return flg

#宿泊旅行の回数と宿泊数
def stying_trip_times_number():
	#データフレーム作成
	sql_list = [sql3,sql4]
	left_list = ['年']
	right_list = ['年']
	df = create_join_df(sql_list, left_list,right_list)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":宿泊旅行の回数と宿泊数"
	x = '年'
	y1 = '回数'
	y2 = '宿泊数'
	df_list = [df]
	legend_list1 = ["回数"]
	legend_list2 = ["宿泊数"]
	times_min =df['宿泊数'].min()
	times_max =df['宿泊数'].max()
	axis = [None,"回数","宿泊数"]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	png_path = file.png_export_path("stying_trip_times_number")
	excel_path = file.excel_export_path("stying_trip_times_number")
	col_del = []
	sheet_name='宿泊旅行の回数と宿泊数'
	position = "B" + str(len(df) + 5)
	index_flg = False
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df)
	return flg

#宿泊旅行の単価と宿泊数
def staying_trip_price_number():
	#データフレーム作成
	sql_list = [sql1,sql4]
	category = "宿泊旅行"
	df = sort_category(sql_list, category)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":宿泊旅行の単価と宿泊数"
	x = '年'
	y1 = '単価'
	y2 = '宿泊数'
	df_list = [df]
	legend_list1 = ["単価"]
	legend_list2 = ["宿泊数"]
	times_min =df['宿泊数'].min()
	times_max =df['宿泊数'].max()
	axis = [None,"単価","宿泊数"]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	png_path = file.png_export_path("staying_trip_price_number")
	excel_path = file.excel_export_path("staying_trip_price_number")
	col_del = []
	sheet_name='宿泊旅行の単価と宿泊数'
	position = "B" + str(len(df) + 5)
	index_flg = False
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df)
	return flg

#1回あたりの旅行単価
def unit_price():
	#データフレーム作成
	df = com_pd.get_table((sql1))
	df1 = df.loc[df['種類']=="日帰り"]
	df2 = df.loc[df['種類']=="宿泊旅行"]
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":1回あたりの旅行単価"
	x = '年'
	y1 = '単価'
	y2 = None
	df_list = [df1,df2]
	legend_list1 = ["日帰り","宿泊旅行"]
	legend_list2 = None
	times_min =None
	times_max =None
	axis = [None,"単価",None]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	png_path = file.png_export_path("unit_price")
	excel_path = file.excel_export_path("unit_price")
	col_del = []
	sheet_name='1回あたりの旅行単価'
	position = "B" + str(len(df) + 5)
	index_flg = False
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df)
	return flg

#1人当たりの旅行回数
def times():
	#データフレーム作成
	sql_list1 = [sql1,sql2]
	sql_list2 = [sql1,sql3]
	category1 = '日帰り'
	category2 = '宿泊旅行'
	df1 = sort_category(sql_list1,category1)
	df2 = sort_category(sql_list2,category2)
	df_list = [df1,df2]
	df = com_pd.concat_df(df_list)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":1人当たりの旅行回数"
	x = '年'
	y1 = '回数'
	y2 = None
	legend_list1 = ["日帰り","宿泊旅行"]
	legend_list2 = None
	times_min =None
	times_max =None
	axis = [None,"回数",None]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	png_path = file.png_export_path("times")
	excel_path = file.excel_export_path("times")
	col_del = ['単価']
	sheet_name='1人当たりの旅行回数'
	position = "B" + str(len(df) + 5)
	index_flg = False
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df)
	return flg
