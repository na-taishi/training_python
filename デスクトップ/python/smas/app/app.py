import config
import common
import logic
from common import dbconnection as db
from config import file_conf as file


##実行ファイル##

#データ準備
def data_preparation():
	flg = logic.preparation.excel_capturing()
	print("データ準備",end=":")
	print(flg)

#祝日登録
def holiday_registration():
	flg = logic.preparation.holiday_registration()
	print("祝日登録",end=":")
	print(flg)

#天気データ登録
def weather_data():
	flg = logic.preparation.weather_data()
	print("天気データ登録",end=":")
	print(flg)

#日帰り旅行の単価と回数
def day_trip():
	flg = logic.one_per.day_trip()
	print("日帰り旅行の単価と回数",end=":")
	print(flg)

#宿泊旅行の単価と回数
def staying_trip_price_times():
	flg = logic.one_per.staying_trip_price_times()
	print("宿泊旅行の単価と回数",end=":")
	print(flg)

#宿泊旅行の回数と宿泊数
def stying_trip_times_number():
	flg = logic.one_per.stying_trip_times_number()
	print("宿泊旅行の回数と宿泊数",end=":")
	print(flg)

#宿泊旅行の単価と宿泊数
def staying_trip_price_number():
	flg = logic.one_per.staying_trip_price_number()
	print("宿泊旅行の単価と宿泊数",end=":")
	print(flg)

#1回あたりの旅行単価
def unit_price():
	flg = logic.one_per.unit_price()
	print("1回あたりの旅行単価",end=":")
	print(flg)

#1人当たりの旅行回数
def times():
	flg = logic.one_per.times()
	print("1人当たりの旅行回数",end=":")
	print(flg)

#年別取扱金額
def yearly_amount():
	flg = logic.handling.yearly_amount()
	print("年別取扱金額",end=":")
	print(flg)

#年別取扱人数
def yearly_count():
	flg = logic.handling.yearly_count()
	print("年別取扱人数",end=":")
	print(flg)

#取扱金額と人数の総数
def handling_total():
	flg = logic.handling.handling_total()
	print("取扱金額と人数の総数",end=":")
	print(flg)

#取扱金額と人数の年月別
def monthly():
	flg = logic.handling.monthly()
	print("取扱金額と人数の年月別",end=":")
	print(flg)

#取扱金額予測
def handling_price_screen():
	common.screen_creation.handling_price_screen()

#月毎の取扱金額予測
def monthly_sales_screen():
	flg = logic.prediction.monthly_sales()
	print("月毎の取扱金額予測",end=":")
	print(flg)

#---実行---#
# #データ準備
# data_preparation()
#祝日登録
# holiday_registration()
#天気データ登録
# weather_data()
# #日帰り旅行の単価と回数
# day_trip()

# #宿泊旅行の単価と回数
# staying_trip_price_times()
# #宿泊旅行の回数と宿泊数
# stying_trip_times_number()
# #宿泊旅行の単価と宿泊数
# staying_trip_price_number()
# #1回あたりの旅行単価
# unit_price()
# #1人当たりの旅行回数
# times()
# #年別取扱金額
# yearly_amount()
# #年別取扱人数
# yearly_count()
# #取扱金額と人数の総数
# handling_total()
# #取扱金額と人数の年月別
# monthly()
#取扱金額予測
# handling_price_screen()
#月毎の取扱金額予測
# monthly_sales_screen()