import datetime
from datetime import timedelta
import locale

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
import statsmodels.api as sm
import statsmodels.formula.api as smf

import config
import common
import logic
from config import file_conf as file
from config.color_conf import COLOR as COLOR
from common import pandas_data as com_pd
from common import graph as graph

####


sql1 =common.db_sql.sql_dict["取扱状況"]
sql2 =common.db_sql.sql_dict["祝日"]
sql3 =common.db_sql.sql_dict["天気"]

#気温データ取得
def get_weather():
	df = common.pandas_data.get_table(sql3)
	df['年'] = df['年月日'].dt.year
	df['月'] = df['年月日'].dt.month
	return df

#年月の平均気温集計
def mean_weather(df,area_flg):
	if area_flg == 1:
		col_list = ['年','月','地域','平均気温','最高気温','最低気温']
		group_list = ['年','月','地域']
	else:
		col_list = ['年','月','平均気温','最高気温','最低気温']
		group_list = ['年','月']
	df_group = df[col_list].groupby(group_list,as_index=False).mean()
	return df_group


#トレーニング用データをリストで取得
# @df:データフレーム
# @num:col_nameの要素数(None:1次元配列、数値：2次元配列)
# @col_name:カラム名(複数の時はリスト)
def get_train_data(df,num,col_name):
	if not num:
		train_data = df[col_name].values
	else:
		train_data = df[col_name].values.reshape(len(df),num)
	train_data
	return train_data

#switch_sales関数からグラフ作成
def sales(pred_value,title,X_col,y_col,axis,png_path,excel_path,sheet_name,legend_list,add_color,add_legend,is_circle,col_del,index_flg):
	#データフレーム作成
	df = com_pd.get_table(sql1)
	#説明変数と目的変数を用意
	X_num = 1
	y_num = None
	X = get_train_data(df,X_num,X_col)
	y = get_train_data(df,y_num,y_col)
	#学習
	model = LinearRegression ()
	model.fit(X,y)
	#予測
	pred_min = df[X_col].min()
	pred_max = df[X_col].max()
	X_axis = [[pred_value],[pred_min],[pred_max]]
	y_pred = model.predict(X_axis)
	#グラフ作成
	df_list = [df]
	fig = graph.create_scatter(df_list, title, X_col, y_col, legend_list, axis)
	#予測グラフ作成
	fig = graph.add_line(fig,X_axis, y_pred, add_color, add_legend, is_circle)
	#データフレーム作成
	digits = len(str(pred_max))
	index_list = [pred_value]
	pred_list = [y_pred[0]]
	trun_val_list = [np.trunc(y_pred[0])]
	count = 2
	for i in range(digits+9):
		num = 10 ** i
		#最大値の桁数から2倍、3倍、...にする
		if len(str(num)) <= digits:
			if i < len(str(pred_min))-2:
				continue
			index_list.append(num)
			pred_list.append(model.predict([[num]])[0])
			trun_val_list.append((np.trunc(model.predict([[num]])[0])))
			tmp_num = num
		else:
			num = tmp_num * count
			count += 1
			index_list.append(num)
			pred_list.append(model.predict([[num]])[0])
			trun_val_list.append((np.trunc(model.predict([[num]])[0])))
	df_pred = pd.DataFrame({X_col:index_list,y_col:pred_list,'小数点切り捨て':trun_val_list})
	# df_pred = pd.DataFrame(data=[pred_list], index=index_list, columns=[y_col])
	#エクセルファイル出力
	values = [y_pred[0],pred_value]
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df_pred)
	return flg

#取扱金額予測
def switch_sales(switch,pred_value):
	#switch変数は入力する値の名前
	if switch == "取扱額":
		title = "取扱金額予測(取扱額)"
		X_col = '取扱額'
		y_col = '取扱人数（人）'
		axis = ["取扱額","取扱人数（人）"]
		png_path = file.png_export_path("sales_amount")
		excel_path = file.excel_export_path("sales_amount")
	elif switch == "取扱人数（人）":
		title = "取扱金額予測(取扱人数)"
		X_col = '取扱人数（人）'
		y_col = '取扱額'
		axis = ["取扱人数（人）","取扱額"]
		png_path = file.png_export_path("sales_count")
		excel_path = file.excel_export_path("sales_count")
	#共通設定
	sheet_name = "予測金額"
	legend_list = "実測値"
	add_color = None
	add_legend ="予測値"
	is_circle = None
	col_del = []
	index_flg = False
	flg = sales(pred_value,title,X_col,y_col,axis,png_path,excel_path,sheet_name,legend_list,add_color,add_legend,is_circle,col_del,index_flg)
	return flg

#曜日取得
def get_weekday(dt):
	locale.setlocale(locale.LC_TIME,'ja_JP.UTF-8')
	wd = dt.strftime('%a')
	return wd

#休日の追加
def add_holiday(df):
	#一般的な夏季休暇、年末年始休暇作成
	years = df['年月日'].dt.year.unique()
	hday_names = ["夏季休暇","年末年始休暇"]
	sv = ["8月13日","8月14日","8月15日"]
	yv = ["1月2日","1月3日","12月29日","12月30日","12月31日"]
	rows = []
	for year in years:
		for name in hday_names:
			if name == "夏季休暇":
				dt_list = sv
			else:
				dt_list = yv
			for dt_str in dt_list:
				dt_str = str(year) + "年" + dt_str
				dt_date = datetime.datetime.strptime(dt_str,'%Y年%m月%d日')
				wday = get_weekday(dt_date)
				row = [dt_date,wday,name]
				rows.append(row)
	col_list = ['年月日','曜日','祝日名']
	add_df = pd.DataFrame(data=rows,columns=col_list)
	#結合
	df_list = [df,add_df]
	df_concat = com_pd.concat_df(df_list).sort_values(by='年月日').reset_index(drop=True)
	return df_concat

#年月カラムの追加
def add_year_month(df,col_names):
	years = df['年'].unique()
	months = df['月'].unique()
	for year in years:
		for month in months:
			dt = str(year) + "-" + str(month)
			df.loc[(df['年']==year) & (df['月']==month),'年月'] = dt
	df_reindex = df.reindex(columns=col_names)
	return df_reindex


#3連休以上のカラムと祝日数のカラム追加
def add_flg(df):
	#3連休以上ありは1、なしは0
	df.loc[(df['曜日']== "金") | (df['曜日']== "月"),'ct_flg'] = 1
	date_list = df['年月日'].values
	tmp_date = None
	count = 0
	for i in date_list:
		if i - np.timedelta64(1,'D') == tmp_date:
			count += 1
			if count == 2:
				count = 0
				df.loc[df['年月日']== i,'ct_flg'] = 1
		else:
			count = 0
		tmp_date = i
	df.fillna(0,inplace=True)
	#年、月カラム作成
	df['年'] = df['年月日'].dt.year
	df['月'] = df['年月日'].dt.month
	#祝日の数をカウント
	df_loc = df.loc[df['祝日名']!="振替休日"]
	col_names1 = ['年','月','祝日名']
	group1 =  ['年','月']
	df_count = df_loc[col_names1].groupby(group1,as_index=False).count()
	df_count.rename(columns={'祝日名':'祝日数'},inplace=True)
	#月毎の連休の有無
	col_names2 = ['年','月','ct_flg']
	group2 =  ['年','月']
	df_sum = df[col_names2].groupby(group2,as_index=False).sum()
	df_sum.loc[df_sum['ct_flg']>=1,'ct_flg'] = 1
	#結合
	df_groups = [df_count,df_sum]
	left_list =  [['年','月']]
	right_list = left_list
	df_join = com_pd.join_df(df_groups, left_list, right_list)
	return df_join

#祝日のない月をセットしたデータフレーム作成
def set_month_df(year):
	df = common.pandas_data.get_table(sql2)
	df_hd = add_holiday(df)
	df_flg = add_flg(df_hd)
	#SettingWithCopyWarningを出さないために。コピーしたものを代入する
	df_year = df_flg.loc[df_flg['年']==year].copy()
	#祝日のない月の取得
	months = np.arange(1,13)
	del_months = []
	for month in months:
		if len(df_year.loc[df_year['月']==month]) == 1:
			del_months.append(month)
	for del_month in del_months:
		months = np.delete(months, np.where(months==del_month))
	#行の追加
	for month in months:
		df_year.loc[len(df_year)]=[year,month,0,0]
	df_sort = df_year.sort_values('月')
	return df_sort

#月毎の取扱金額予測
def monthly_sales():
	#データフレーム作成
	df1 = com_pd.get_table(sql1)
	df2 = com_pd.get_table(sql2)
	df2 = add_holiday(df2)
	df2 = add_flg(df2)
	df_weather = get_weather()
	#結合
	df_list = [df1,df2]
	left_list =  [['年','月']]
	right_list = left_list
	df_join = com_pd.left_join_df(df_list, left_list, right_list)
	df_join.fillna(0,inplace=True)
	#説明変数と目的変数を用意
	x = df_join[['年','月','祝日数','ct_flg']]
	y = df_join['取扱額']
	# X = sm.add_constant(x)
	X = x
	#学習
	model = sm.OLS(y, X)
	result = model.fit()
	# print(result.summary())
	pred_year = 2020
	pred_df_list = [set_month_df(pred_year)]
	X_pred = com_pd.left_join_df(pred_df_list, left_list, right_list)
	#predictの引数はmodelのXの要素数に合わせる
	y_pred = result.predict(X_pred)
	#グラフ作成
	df_list = [df_join]
	X_col = '月'
	y_col = '取扱額'
	title = "test"
	legend_list = "実測値"
	axis = ["月","取扱額"] 
	fig = graph.create_scatter(df_list, title, X_col, y_col, legend_list, axis)
	#去年の実績グラフ
	year_max = df_join['年'].max()
	if year_max == pred_year:
		last_year = pred_year - 1
	else:
		last_year =year_max
	x_axis = df_join.loc[df_join['年']==last_year]['月']
	y_axis = df_join.loc[df_join['年']==last_year]['取扱額']
	add_color = COLOR(11)
	add_legend = str(last_year) + "年の" + "実測値"
	is_circle = None
	fig = graph.add_line(fig,x_axis, y_axis, add_color, add_legend, is_circle)
	#予測グラフ作成
	X_axis = X_pred['月']
	add_color = "red"
	add_legend = str(pred_year)+ "年の" + "予測値"
	is_circle = None
	fig = graph.add_line(fig,X_axis, y_pred, add_color, add_legend, is_circle)
	#エクセル出力用のデータ作成
	idx_amt = str(pred_year)+"年の取扱金額"
	idx_last_amt = str(last_year)+"年の取扱金額"
	index = [idx_amt,idx_last_amt]
	columns = np.sort(df1['月'].unique())
	data = [y_pred.values,y_axis.values]
	df_excel = pd.DataFrame(data = data, index = index, columns = columns)
	#エクセルファイル出力
	png_path = file.png_export_path("monthly_sales")
	excel_path = file.excel_export_path("monthly_sales")
	col_del = []
	sheet_name = "月毎の取扱金額予測"
	index_flg = True
	flg =common.excel.export_excel(fig, png_path, excel_path, col_del, sheet_name,index_flg, df_excel)
	return flg