import os

import pandas as pd
import numpy as np

import config
import common
import logic
from common import dbconnection as db
from config import file_conf as file

#現在位置
# print('getcwd:      ', os.getcwd())


# sql1 = common.db_sql.sql_dict["1人当たりの宿泊数"]
# sql2 = common.db_sql.sql_dict["1人当たりの宿泊旅行回数"]

# df1 = common.pandas_data.get_table(sql1)
# df2 = common.pandas_data.get_table(sql2)
# print(df1)
# print(df2)

# df_list = [df1,df2]
# l = ['年']
# r = ['年']
# # df = common.pandas_data.join_df(df_list,l,r)
# # print(df)
# df = common.pandas_data.concat_df(df_list)
# print(df)

# excel_path = config.file_conf.excel_import_path("excel_capturing")
# flg = common.excel.paste_image("excel_path","img_path","position")
# p = logic.popularity_ranking.trip_target_total()
# p = logic.one_per.staying_trip_price_times()
# p = logic.one_per.staying_trip()
# p = logic.one_per.stying_trip_times_number()
# p = logic.one_per.staying_trip_price_number()
# p = logic.one_per.unit_price()
# p = logic.one_per.times()
# p = logic.handling.yearly_amount()
# p = logic.handling.yearly_count()
# p = logic.handling.handling_total()
# p = logic.handling.monthly()
# p = logic.popularity_ranking.trip_target_by_time()
# p = logic.prediction.switch_sales()
# logic.prediction.test()
# common.screen_creation.create_screen()

# year = "2011"
# url = "http://www.technosquare.co.jp/appendix/holiday.html?year=" + year
# class_name = "type1"
# split_str = '[（）\n]'
# num = 3
# p = common.web_scraping.get_class(url,class_name,split_str,num)
# print(p)

# p = logic.preparation.holiday_registration()
# p = logic.prediction.create_df_holiday()
# p = logic.prediction.monthly_sales()
# p = logic.prediction.pred_data(2020)
# print(p)

# flg = common.screen_creation.test()
# print(flg)

# ym_li = logic.temperature_analysis.join_season()
# ym_li = logic.temperature_analysis.set_temperature_flg(ym_li)
# ym_li = logic.temperature_analysis.set_earthquake_flg(ym_li)
# ym_li = logic.temperature_analysis.add_good_flg(ym_li)
# ym_li = logic.temperature_analysis.add_demand_flg(ym_li)
# ym_li = logic.temperature_analysis.aggregate(ym_li)
# print(ym_li)


# logic.temperature_analysis.export_excel(ym_li)
# p = logic.temperature_analysis.predict_temperature(20,25,16,0,60,"ゴールデンウィーク")
# print(p[0])
# flg = logic.preparation.earthquake_data()
# print(flg)

weather_df = logic.temperature_analysis.join_weather()
# ptrip_df =logic.temperature_analysis.get_popular_trip()
# join_df = logic.temperature_analysis.join_season(weather_df,ptrip_df)
# df_list = logic.temperature_analysis.divide_season(join_df)
# #平均気温,最高気温,最低気温,最大震度,平均湿度,時期,地域
# x_name = "平均気温"
# y_name = "最高気温"
# label_name = "時期"
# png_flg = logic.temperature_analysis.export_png(df_list,x_name,y_name,label_name)
# excel_flg = logic.temperature_analysis.export_excel(join_df)
# print(excel_flg)


# pr = common.pptx_operation.exec_pptx()
# print(pr)

common.pptx_operation.create_chart(weather_df)
