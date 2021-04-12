import numpy as np
import pandas as pd

import config
import common
from config import file_conf as file
from common import pandas_data as com_pd

##人気の旅行先ランキング##


sql = common.db_sql.sql_dict["人気の旅行先"]


#順位ごとにポイント付与
def add_point(df):
	rank_np = np.sort(df['順位'].unique())[::-1]
	for count,rank in enumerate(rank_np,1):
		df.loc[df['順位']==rank,'point'] = count

#集計して、ソートする
def sort_group(df,col_list,group):
	df_groupby = df[col_list].groupby(group,as_index=False).sum()
	df_sort = df_groupby.sort_values(by='point', ascending=False).reset_index(drop=True)
	return df_sort

#順位付け
def ranking(df):
	tmp_value = None
	for count,value in enumerate(df['point'].values,1):
		if tmp_value == value:
			continue
		df.loc[df['point'] == value,'順位']  = count
		tmp_value = value

#集計して、順位の振り直し
def add_rank(df,col_list,group):
	add_point(df)
	df_sort = sort_group(df,col_list,group)
	ranking(df_sort)
	return df_sort

#人気の旅行先(累計)
def trip_target_total():
	df = com_pd.get_table(sql)
	#「年」の最小値と最大値取得
	year_min = df['年'].min()
	year_max = df['年'].max()
	#集計して、順位の振り直し
	col_list = ['旅行先','point']
	group = '旅行先'
	df_sort = add_rank(df,col_list,group)
	#グラフ作成
	title = str(year_min) + "~" + str(year_max) + ":人気の旅行先(累計)"
	x = '旅行先'
	y = 'point'
	fig = common.graph.create_bar(df_sort,title,x,y)
	#エクセルファイル出力
	png_path = file.png_export_path("trip_target_total")
	excel_path = file.excel_export_path("trip_target_total")
	col_del = ['point']
	sheet_name='人気の旅行先(累計)'
	position = "B" + str(len(df_sort) + 5)
	index_flg = False
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df_sort)
	return flg

# #人気の旅行先(時期別)
# def trip_target_by_time():
# 	df = com_pd.get_table(sql)
# 	values = df['時期'].unique()
# 	col_name = '時期'
# 	df_list = com_pd.create_df_list(df, values, col_name)
# 	#「年」の最小値と最大値取得
# 	year_min = df['年'].min()
# 	year_max = df['年'].max()
# 	#集計して、順位の振り直し
	
# 	#グラフ作成
# 	# title = str(year_min) + "~" + str(year_max) + ":人気の旅行先(時期別)"
# 	# x = '旅行先'
# 	# y = '年'
# 	# fig = common.graph.create_bar(df,title,x,y)
# 	# #エクセルファイル出力
# 	# png_path = file.png_export_path("trip_target_by_time")
# 	# excel_path = file.excel_export_path("trip_target_by_time")
# 	# col_del = None
# 	# sheet_name='人気の旅行先(時期別)'
# 	# position = "B" + str(len(df) + 5)
# 	# index_flg = False
# 	# flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df)

# 	return df
