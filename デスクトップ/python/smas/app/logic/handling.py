import numpy as np
import pandas as pd

import config
import common
from config import file_conf as file
from common import pandas_data as com_pd

##取扱金額と人数##

sql =common.db_sql.sql_dict["取扱状況"]

#指定したカラムの数が合わないときにデータの切り捨て
def truncate_df(col_name,num):
	df = com_pd.get_table(sql)
	type_list = df[col_name].unique()
	for i in type_list:
		tmp_df = df.loc[df[col_name]==i]
		if len(tmp_df) != num:
			df = df.loc[df[col_name]!=i]
	return df

#集計
def group_sum(col_list,group):
	col_name = '年'
	num = 12
	df = truncate_df(col_name,num).reset_index(drop=True)
	df_groupby = df[col_list].groupby(group,as_index=False).sum()
	return df_groupby

#クロス集計
def pivot_sum(df,col_list,pivot_list):
	df_pivot = df[col_list].pivot_table(index=pivot_list[0],columns=pivot_list[1],values=pivot_list[2],aggfunc='sum',margins=True,margins_name='合計')
	return df_pivot

#年別取扱金額
def yearly_amount():
	#データフレーム作成
	col_name = '年'
	num = 12
	df = truncate_df(col_name,num).reset_index(drop=True)
	year_np = df['年'].unique()
	df_list = com_pd.create_df_list(df, year_np, col_name)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":年別取扱金額"
	x = '月'
	y1 = '取扱額'
	y2 = None
	legend_list1 = year_np.astype('str')
	legend_list2 = None
	times_min =None
	times_max =None
	axis = ["月","取扱額",None]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	col_list = ['年','月','取扱額']
	pivot_list =  ['年','月','取扱額']
	df_pivot = pivot_sum(df,col_list,pivot_list)
	png_path = file.png_export_path("yearly_amount")
	excel_path = file.excel_export_path("yearly_amount")
	col_del = None
	sheet_name='年別取扱金額'
	position = "B" + str(len(df) + 5)
	index_flg = True
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df_pivot)
	return flg

#年別取扱人数
def yearly_count():
	#データフレーム作成
	col_name = '年'
	num = 12
	df = truncate_df(col_name,num).reset_index(drop=True)
	year_np = df['年'].unique()
	df_list = com_pd.create_df_list(df, year_np, col_name)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":年別取扱人数"
	x = '月'
	y1 = '取扱人数（人）'
	y2 = None
	legend_list1 = year_np.astype('str')
	legend_list2 = None
	times_min =None
	times_max =None
	axis = ["月","取扱人数（人）",None]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	col_list = ['年','月','取扱人数（人）']
	pivot_list =  ['年','月','取扱人数（人）']
	df_pivot = pivot_sum(df,col_list,pivot_list)
	png_path = file.png_export_path("yearly_count")
	excel_path = file.excel_export_path("yearly_count")
	col_del = None
	sheet_name='年別取扱人数'
	position = "B" + str(len(df) + 5)
	index_flg = True
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df_pivot)
	return flg

#取扱金額と人数の総数
def handling_total():
	#データフレーム作成
	col_list = ['年','取扱額','取扱人数（人）']
	group = '年'
	df = group_sum(col_list,group)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":取扱金額と人数の総数"
	x = '年'
	y1 = '取扱額'
	y2 = '取扱人数（人）'
	legend_list1 = ["取扱額"]
	legend_list2 = ["取扱人数（人）"]
	times_min =df['取扱人数（人）'].min()
	times_max =df['取扱人数（人）'].max()
	axis = ["年","取扱額","取扱人数（人）"]
	df_list = [df]
	fig = common.graph.create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,times_min,times_max,axis)
	#エクセルファイル出力
	png_path = file.png_export_path("handling_total")
	excel_path = file.excel_export_path("handling_total")
	col_del = None
	sheet_name='取扱金額と人数の総数'
	position = "B" + str(len(df) + 5)
	index_flg = False
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df)
	return flg

#取扱金額と人数の年月別
def monthly():
	#データフレーム作成
	col_name1 = '年'
	num = 12
	df = truncate_df(col_name1,num).reset_index(drop=True)
	col_name2 = '月'
	month_np = df['月'].unique()
	df_list = com_pd.create_df_list(df,month_np,col_name2)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":取扱金額と人数の年月別"
	x = '取扱人数（人）'
	y = '取扱額'
	legend_list = month_np.astype('str')
	axis = ["取扱人数（人）","取扱額",None]
	fig = common.graph.create_scatter(df_list,title,x,y,legend_list,axis)
	#エクセルファイル出力
	col_list = ['年','月','取扱額','取扱人数（人）']
	pivot_list =  ['年','月',['取扱額','取扱人数（人）']]
	df_pivot = pivot_sum(df,col_list,pivot_list)
	png_path = file.png_export_path("monthly")
	excel_path = file.excel_export_path("monthly")
	col_del = None
	sheet_name='取扱金額と人数の年月別'
	position = "B" + str(len(df) + 5)
	index_flg = True
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df_pivot)
	return flg