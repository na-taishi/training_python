import time
import glob

import numpy as np
import pandas as pd

import common
import config
from config import file_conf as file

##データ準備##

#excelファイルをテーブルに出力
def excel_capturing():
	flg = True
	path = config.file_conf.excel_import_path("excel_capturing")
	#シートの中身と名前を取得
	excel_data = common.pandas_data.get_excel(path)
	df_dict = excel_data[0]
	sheet_name_list = excel_data[1]
	#テーブルに出力
	for sheet_name in sheet_name_list:
		df = df_dict[sheet_name]
		#テーブル名が設定されていないシート名の場合
		tbl_dict = config.tbl_conf.tbl_dict
		if sheet_name in tbl_dict:
			tbl_name = config.tbl_conf.tbl_dict[sheet_name]
			db_flg = common.pandas_data.export_table(df,tbl_name)
		else:
			tbl_name = sheet_name
			db_flg = common.pandas_data.export_table(df,tbl_name)
		if db_flg == False:
			flg = db_flg
	return flg

#祝日登録
def holiday_registration():
	#スクレイピング準備
	years = list(range(2010,2031))
	years_str = [str(i) for i in years]
	class_name = "type1"
	split_str = '[（）\n]'
	num = 3
	col_list = ['年月日','曜日','祝日名']
	df_list = []
	#年毎にデータフレーム作成
	for year in years_str:
		url = "http://www.technosquare.co.jp/appendix/holiday.html?year=" + year
		rows = common.web_scraping.get_class(url,class_name,split_str,num)
		#データフレーム作成と日付型に変換
		df = pd.DataFrame(data=rows,columns=col_list)
		df['年月日'] = year + "年" + df['年月日']
		df['年月日'] = pd.to_datetime(df['年月日'],format='%Y年%m月%d日')
		df_list.append(df)
		#3秒待つ
		time.sleep(3)
	df_concat = common.pandas_data.concat_df(df_list)
	#テーブルに出力
	tbl_name = "holiday"
	flg = common.pandas_data.export_table(df_concat,tbl_name)
	return flg

#天気データ登録
def weather_data():
	#CSV読み込み
	path = file.import_path_dict["weather_data"] + "天気データ/"
	exc = "csv"
	header = 1
	df_list = common.pandas_data.read_dir(path,exc,header)
	#地域設定
	area_dict = {
	"小田原":"伊豆、箱根",
	"那覇":"沖縄",
	"京都":"京都",
	"博多":"九州",
	"大阪":"大阪",
	"東京":"東京",
	"千歳":"北海道",
	"金沢":"北陸"
	}
	#カラム設定
	col_names = ['年月日','地域','平均気温','最高気温','最低気温']
	#カラム名の変更や削除をして、結合する
	df_wh = []
	for i in df_list:
		i['地域'] = area_dict[i.columns.values[1]]
		rename_dict = {
		i.columns.values[0]:col_names[0],
		i.columns.values[1]:col_names[2],
		i.columns.values[4]:col_names[3],
		i.columns.values[7]:col_names[4]
		}
		i.rename(columns=rename_dict, inplace=True)
		i.drop(i.index[[0,1,2]],inplace=True)
		i = i[col_names] 
		df_wh.append(i)
	df = common.pandas_data.concat_df(df_wh)
	df.reset_index(inplace=True, drop=True)
	df['年月日'] = pd.to_datetime(df['年月日'], format='%Y/%m/%d')
	df[['平均気温','最高気温','最低気温']] = df[['平均気温','最高気温','最低気温']].astype('float64')
	#テーブルに出力
	tbl_name = "weather"
	flg = common.pandas_data.export_table(df,tbl_name)
	return flg

#湿度データ登録
def humidity_data():
	#CSV読み込み
	path = file.import_path_dict["weather_data"] + "湿度データ/"
	exc = "csv"
	header = 1
	df_list = common.pandas_data.read_dir(path,exc,header)
	#地域設定
	area_dict = {
	"三島":"伊豆、箱根",
	"那覇":"沖縄",
	"京都":"京都",
	"福岡":"九州",
	"大阪":"大阪",
	"東京":"東京",
	"札幌":"北海道",
	"金沢":"北陸"
	}
	#カラム設定
	col_names = ['年月日','地域','平均湿度','最小相対湿度','平均風速','最大風速','最大瞬間風速']
	#カラム名の変更や削除をして、結合する
	df_hd = []
	for i in df_list:
		i['地域'] = area_dict[i.columns.values[1]]
		rename_dict = {
		i.columns.values[0]:col_names[0],
		i.columns.values[1]:col_names[2],
		i.columns.values[4]:col_names[3],
		i.columns.values[7]:col_names[4],
		i.columns.values[10]:col_names[5],
		i.columns.values[15]:col_names[6],
		}
		i.rename(columns=rename_dict, inplace=True)
		i.drop(i.index[[0,1,2]],inplace=True)
		i = i[col_names] 
		i.fillna(0,inplace=True)
		df_hd.append(i)
	df = common.pandas_data.concat_df(df_hd)
	df.reset_index(inplace=True, drop=True)
	df['年月日'] = pd.to_datetime(df['年月日'], format='%Y/%m/%d')
	df[['平均湿度','最小相対湿度']] = df[['平均湿度','最小相対湿度']].astype('int64')
	df[['平均風速','最大風速','最大瞬間風速']] = df[['平均風速','最大風速','最大瞬間風速']].astype('float64')
	#テーブルに出力
	tbl_name = "humidity"
	flg = common.pandas_data.export_table(df,tbl_name)
	return flg

#地震データ登録
def earthquake_data():
	#CSV読み込み
	path = file.import_path_dict["earthquake_data"] + "地震データ/"
	exc = "csv"
	header = 0
	df_list = common.pandas_data.read_dir(path,exc,header)
	#結合
	df = common.pandas_data.concat_df(df_list)
	df['発生日'] = pd.to_datetime(df['発生日'], format='%Y/%m/%d')
	#テーブルに出力
	tbl_name = "earthquake"
	flg = common.pandas_data.export_table(df,tbl_name)
	return flg