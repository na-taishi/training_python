import re

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import config
import common
import logic
from config import file_conf as file
from config.color_conf import COLOR as COLOR

##気温と人気の旅行先の関係

#地域を取得(重複なし)
sql_local = "SELECT DISTINCT 地域 FROM weather;"
#日付取得
sql_date = "SELECT 年月日 FROM weather;"
#指定年月の平均気温取得
sql_avg = "SELECT 地域,AVG(平均気温) AS 平均気温 FROM weather WHERE EXTRACT(YEAR from 年月日) = %(year)s AND EXTRACT(MONTH from 年月日) = %(month)s  GROUP BY 地域;"
#指定年月の最高気温取得
sql_max = "SELECT 地域,MAX(最高気温) AS 最高気温 FROM weather WHERE EXTRACT(YEAR from 年月日) = %(year)s AND EXTRACT(MONTH from 年月日) = %(month)s GROUP BY 地域;"
#指定年月の最低気温取得
sql_min = "SELECT 地域,MIN(最低気温) AS 最低気温 FROM weather WHERE EXTRACT(YEAR from 年月日) = %(year)s AND EXTRACT(MONTH from 年月日) = %(month)s GROUP BY 地域;"
#人気の旅行先
sql_ptrip = common.db_sql.sql_dict["人気の旅行先"]
#地震データ
sql_earthquake = common.db_sql.sql_dict["地震"]
#湿度データ
sql_humidity = common.db_sql.sql_dict["湿度"]


#地震データを加工
def transform_earthquake():
	df = common.pandas_data.get_table(sql_earthquake)
	df['最大震度'] = df['最大震度'].str.extract(r'(\d+)').astype(int)
	df['year'] = df['発生日'].dt.year
	df['month'] = df['発生日'].dt.month
	#各地域、月毎の震度の大きいものに絞り込み
	groupby_df = df.groupby(['year','month','地域'])
	max_df = df.loc[groupby_df['最大震度'].idxmax()]
	return max_df

#湿度データを加工
def transform_humidity():
	df = common.pandas_data.get_table(sql_humidity)
	df['year'] = df['年月日'].dt.year
	df['month'] = df['年月日'].dt.month
	#各地域、月毎の平均湿度に絞り込み
	groupby_df = df.groupby(['year','month','地域'])
	mean_df = groupby_df[['平均湿度','平均風速']].mean().reset_index()
	return mean_df

#タイムスタンプを年月に分ける
def get_year_month():
	date_df = common.pandas_data.get_table(sql_date)
	date_df['year'] = date_df['年月日'].dt.year
	date_df['month'] = date_df['年月日'].dt.month
	date_df['year_month'] = date_df['year'].astype(str) + "-" +date_df['month'].astype(str)
	year_list = date_df['year'].unique()
	month_list = date_df['month'].unique()
	result = [year_list,month_list,date_df]
	return result

#各月毎の気温
def get_temperature():
	#年*月ループ
	year_month = get_year_month()
	year_list = year_month[0]
	month_list = year_month[1]
	kion_list = []
	for year in year_list:
		for month in month_list:
			#SQLのパラメータをセット
			avg_par = {"year":str(year),"month":str(month)}
			max_par = {"year":str(year),"month":str(month)}
			min_par = {"year":str(year),"month":str(month)}
			avg_df =common.pandas_data.get_table_par(sql_avg,avg_par)
			max_df =common.pandas_data.get_table_par(sql_max,max_par)
			min_df =common.pandas_data.get_table_par(sql_min,min_par)
			#年と月の列を追加
			min_df['year'] = year
			min_df['month'] = month
			df_list = [avg_df,max_df,min_df]
			kion_list.append(df_list)
	#結合
	vertical_list = []
	left_list = ["地域","地域"]
	right_list = ["地域","地域"]
	for horizontal in kion_list:
		vertical_list.append(common.pandas_data.join_df(horizontal,left_list,right_list))
	join_df = common.pandas_data.concat_df(vertical_list)
	return join_df

#気温、湿度、震度を結合
def join_weather():
	#結合するデータフレームを用意
	temperature_df = get_temperature()
	earthquake_df = transform_earthquake()
	humidity_df = transform_humidity()
	#内部結合
	df_list = [temperature_df,humidity_df]
	left_list = [["year","month","地域"]]
	right_list = [["year","month","地域"]]
	innerjoin_df = common.pandas_data.join_df(df_list,left_list,right_list)
	#外部結合
	df_list = [innerjoin_df,earthquake_df]
	left_list = [["year","month","地域"]]
	right_list = [["year","month","地域"]]
	outerjoin_df = common.pandas_data.left_join_df(df_list,left_list,right_list)
	outerjoin_df.fillna({"マグニチュード":0},inplace=True)
	outerjoin_df.fillna({"最大震度":0},inplace=True)
	join_df = outerjoin_df[['発生日','year', 'month','地域', '平均気温', '最高気温', '最低気温','マグニチュード', '最大震度','平均湿度', '平均風速']]
	return join_df

#気象とランキングを結合
def join_season():
	#結合するデータフレームを用意
	ptrip_df = common.pandas_data.get_table(sql_ptrip)
	weather_df = join_weather()
	#気象データフレームに時期のカラムを追加
	weather_df.loc[(weather_df['month'] == 4) | (weather_df['month'] == 5) ,"時期"] = "ゴールデンウィーク"
	#夏休み(7-8)
	weather_df.loc[(weather_df['month'] == 7) | (weather_df['month'] == 8) ,"時期"] = "夏休み"
	#年末年始(12-1)
	weather_df.loc[(weather_df['month'] == 12) | (weather_df['month'] == 1) ,"時期"] = "年末年始"
	#年度で判定するために、1月の年をマイナス1する
	weather_df.loc[weather_df['month'] == 1,"year"] -= 1
	#前年の気象データと紐づけるようにする
	ptrip_df['年'] -= 1
	#気象データと各連休データを結合
	df_list = [weather_df,ptrip_df]
	left_list = [["year","地域","時期"]]
	right_list = [["年","旅行先","時期"]]
	join_df = common.pandas_data.left_join_df(df_list,left_list,right_list)
	#カラム削除
	del_cols = ["年","旅行先","順位","昨年","発生日","マグニチュード","平均風速"]
	join_df.drop(columns=del_cols,inplace=True)
	return join_df

#時期毎に分ける(未使用)
def divide_season(df):
	col_name = "時期"
	col_values = ["ゴールデンウィーク","夏休み","年末年始"]
	season_df_list = [df.loc[df[col_name] == value] for value in col_values]
	return season_df_list

#快適な気温にフラグを立てる
def set_temperature_flg(df):
	col_names = ["平均気温","最高気温","最低気温"]
	for col_name in col_names:
		df.loc[(df[col_name] >= 16) & (df[col_name] <= 21) & (df['時期'] == "年末年始") ,"{}_flg".format(col_name)] = 1
		df.loc[(df[col_name] >= 18) & (df[col_name] <= 23) & (df['時期'] == "ゴールデンウィーク") ,"{}_flg".format(col_name)] = 1
		df.loc[(df[col_name] >= 20) & (df[col_name] <= 25) & (df['時期'] == "夏休み") ,"{}_flg".format(col_name)] = 1
		df.fillna({"{}_flg".format(col_name):0},inplace=True)
	return df

#規模の大きい地震にフラグを立てる
def set_earthquake_flg(df):
	col_name = "最大震度"
	df.loc[df[col_name] >= 4 ,"{}_flg".format(col_name)] = 1
	df.fillna({"{}_flg".format(col_name):0},inplace=True)
	return df

#集計(確認用)
def aggregate(df):
	groupby_df = df.groupby(['時期']).sum()[['平均気温_flg','最高気温_flg','最低気温_flg','最大震度_flg']]
	print(groupby_df)

#快適な気温のフラグを立てる
def add_good_flg(df):
	season_list = ["ゴールデンウィーク","夏休み","年末年始"]
	temperature_list = ["平均気温_flg","最低気温_flg","最高気温_flg"]
	for count in range(len(season_list)):
		df.loc[(df['時期'] == season_list[count]) & (df[temperature_list[count]] == 1),"good_flg"] = 1
	df.fillna({"good_flg":0},inplace=True)
	return df

#需要フラグを立てる
def add_demand_flg(df):
	season_list = ["ゴールデンウィーク","夏休み","年末年始"]
	for season in season_list:
		df.loc[df['時期'] == season ,"demand_flg"] = 1
	df.fillna({"demand_flg":0},inplace=True)
	df.loc[(df['month'] == 4) & (df['month'] == 5),'時期'] = "ゴールデンウィーク"
	df.loc[(df['month'] == 7) & (df['month'] == 8),'時期'] = "夏休み"
	df.loc[(df['month'] == 12) & (df['month'] == 1),'時期'] = "年末年始"
	return df

#png_test
def export_png(df,x_name,y_name,label_name):
	fig = common.graph_matplotlib.create_scatter(df,x_name,y_name,label_name)
	pmg_path = file.png_export_path("sales_count")
	# common.graph_matplotlib.output_png(fig,pmg_path)

#excel_test
def export_excel(df):
	excel_path = file.excel_export_path("sales_amount")
	sheet_name = "test"
	index_flg = False
	df.to_excel(excel_path, sheet_name=sheet_name,index=index_flg)

#各フラグを付ける(需要フラグ除く)
def add_flg(df):
	temperature_flg_df = set_temperature_flg(df)
	earthquake_flg_df = set_earthquake_flg(temperature_flg_df)
	good_flg_df = add_good_flg(earthquake_flg_df)
	return good_flg_df

#予測したデータ作成
def create_pred_model(val1,val2,val3,val4,val5,val6):
	val_list = [val1,val2,val3,val4,val5,val6]
	col_list = ["平均気温", "最高気温", "最低気温","最大震度","平均湿度","時期"]
	df = pd.DataFrame(data=[val_list],columns=col_list)
	pred_df = add_flg(df)
	pred_df.drop(columns="時期",inplace=True)
	X_pred = pred_df.values
	print(X_pred)
	return X_pred


#機械学習
def predict_temperature():
	join_df = join_season()
	flg_df = add_flg(join_df)
	df = add_demand_flg(flg_df)
	# df = pd.get_dummies(df,drop_first = True,columns=['時期'])
	# df.drop(columns=['地域','year','month'], inplace=True)
	df.drop(columns=['地域','year','month','時期'], inplace=True)
	#目的変数のカラムを削除
	target = "demand_flg"
	train_data = df.drop(target, axis=1)
	y = df[target].values
	X = train_data.values
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)
	clf = RandomForestClassifier(random_state=1234)
	clf.fit(X_train, y_train)
	#精度表示
	print("score=", clf.score(X_test, y_test))
	#'平均気温', '最高気温', '最低気温', '最大震度', '平均湿度', '平均気温_flg', '最高気温_flg','最低気温_flg', '最大震度_flg', 'good_flg'
	X_pred = create_pred_model(20,25,14,0,60,"ゴールデンウィーク")
	y_pred = clf.predict(X_pred)
	# y_pred = clf.predict(X_test)
	print(y_pred)
