#国内旅行宿泊数
sql="SELECT * FROM travel_staying_number;"
#人気の旅行先
sql="SELECT * FROM popular_trip_target;"
#取扱状況
sql="SELECT * FROM handling_status;"
#1回あたりの旅行単価
sql="SELECT * FROM travel_unit_price_per_once;"
#1人当たりの宿泊数
sql="SELECT * FROM staying_number_per_one_person;"
#1人当たりの宿泊旅行回数
sql="SELECT * FROM staying_trip_times_per_one_person;"
#1人当たりの日帰り旅行回数
sql="SELECT * FROM day_trip_times_per_one_person;" 

sql_dict ={
"国内旅行宿泊数":"SELECT * FROM travel_staying_number;",
"人気の旅行先":"SELECT * FROM popular_trip_target;",
"取扱状況":"SELECT * FROM handling_status;",
"1回あたりの旅行単価":"SELECT * FROM travel_unit_price_per_once;",
"1人当たりの宿泊数":"SELECT * FROM staying_number_per_one_person;",
"1人当たりの宿泊旅行回数":"SELECT * FROM staying_trip_times_per_one_person;",
"1人当たりの日帰り旅行回数":"SELECT * FROM day_trip_times_per_one_person;",
"祝日":"SELECT * FROM holiday;",
"天気":"SELECT * FROM weather;",
"地震":"SELECT * FROM earthquake;",
"湿度":"SELECT * FROM humidity;"
}



