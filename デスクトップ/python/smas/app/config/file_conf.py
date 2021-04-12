#ファイル入出力設定
import_path="import/"
export_path="export/"
file_name="投入データ" 


# def import_path_f(fun_name):
# 	path = import_path_dict["fun_name"]
# 	return path

# def export_path(fun_name):
# 	path = export_path_dict["fun_name"]
# 	return path

# def import_name(fun_name):
# 	name = import_name_dict["fun_name"]
# 	return name

# def export_name(fun_name):
# 	name = export_name_dict["fun_name"]
# 	return name

#エクセルの読み込みパス
def excel_import_path(fun_name):
	file_path = import_path_dict[fun_name] + import_name_dict[fun_name] + ".xlsx"
	return file_path

#エクセルの出力パス
def excel_export_path(fun_name):
	file_path = export_path_dict[fun_name] + export_name_dict[fun_name] + ".xlsx"
	return file_path

#PNGの読み込みパス
def png_import_path(fun_name):
	file_path = import_path_dict[fun_name] + import_name_dict[fun_name] + ".png"
	return file_path

#PNGの出力パス
def png_export_path(fun_name):
	file_path = export_path_dict[fun_name] + export_name_dict[fun_name] + ".png"
	return file_path


#読み込むパスの辞書(関数名で値を取得)
import_path_dict ={
	#preparationファイル
	"excel_capturing":import_path,
	"weather_data":import_path,
	"earthquake_data":import_path,
	#popularity_ranking
	"trip_target_total":import_path,
	"trip_target_by_time":import_path,
	#one_per
	"day_trip":import_path,
	"staying_trip_price_times":import_path,
	"stying_trip_times_number":import_path,
	"staying_trip_price_number":import_path,
	"unit_price":import_path,
	"times":import_path,
	#handling
	"yearly_amount":import_path,
	"yearly_count":import_path,
	"handling_total":import_path,
	"monthly":import_path,
	#prediction
	"sales_amount":import_path,
	"sales_count":import_path,
	"monthly_sales":import_path
}

#出力パスの辞書(関数名で値を取得)
export_path_dict ={
	#preparationファイル
	"excel_capturing":export_path,
	"weather_data":export_path,
	"earthquake_data":export_path,
	#popularity_ranking
	"trip_target_total":export_path,
	"trip_target_by_time":export_path,
	#one_per
	"day_trip":export_path,
	"staying_trip_price_times":export_path,
	"stying_trip_times_number":export_path,
	"staying_trip_price_number":export_path,
	"unit_price":export_path,
	"times":export_path,
	#handling
	"yearly_amount":export_path,
	"yearly_count":export_path,
	"handling_total":export_path,
	"monthly":export_path,
	#prediction
	"sales_amount":export_path,
	"sales_count":export_path,
	"monthly_sales":export_path
}

#読み込むファイル名のの辞書(関数名で値を取得)
import_name_dict ={
	#preparationファイル
	"excel_capturing":file_name,
	"weather_data":"",
	#popularity_ranking
	"trip_target_total":file_name,
	"trip_target_by_time":"人気の旅行先(時期別)",
	#one_per
	"day_trip":"日帰り旅行の単価と回数",
	"staying_trip_price_times":"宿泊旅行の単価と回数",
	"stying_trip_times_number":"宿泊旅行の回数と宿泊数",
	"staying_trip_price_number":"宿泊旅行の単価と宿泊数",
	"unit_price":"1回あたりの旅行単価",
	"times":"1人当たりの旅行回数",
	#handling
	"yearly_amount":"年別取扱金額",
	"yearly_count":"年別取扱人数",
	"handling_total":"取扱金額と人数の総数",
	"monthly":"取扱金額と人数の年月別",
	#prediction
	"sales_amount":"取扱金額予測(取扱額)",
	"sales_count":"取扱金額予測(取扱人数)",
	"monthly_sales":"月毎の取扱金額予測"
}

#出力ファイル名の辞書(関数名で値を取得)
export_name_dict ={
	#preparationファイル
	"excel_capturing":"",
	"weather_data":"",
	#popularity_ranking
	"trip_target_total":"人気の旅行先(累計)",
	"trip_target_by_time":"人気の旅行先(時期別)",
	#one_per
	"day_trip":"日帰り旅行の単価と回数",
	"staying_trip_price_times":"宿泊旅行の単価と回数",
	"stying_trip_times_number":"宿泊旅行の回数と宿泊数",
	"staying_trip_price_number":"宿泊旅行の単価と宿泊数",
	"unit_price":"1回あたりの旅行単価",
	"times":"1人当たりの旅行回数",
	#handling
	"yearly_amount":"年別取扱金額",
	"yearly_count":"年別取扱人数",
	"handling_total":"取扱金額と人数の総数",
	"monthly":"取扱金額と人数の年月別",
	#prediction
	"sales_amount":"取扱金額予測(取扱額)",
	"sales_count":"取扱金額予測(取扱人数)",
	"monthly_sales":"月毎の取扱金額予測"
}