import shutil
import datetime

from flask import Flask,render_template,request,redirect,send_from_directory

import logic
from config import file_conf as file


app = Flask(__name__)

#pngファイルのコピー
def pngfile_copy(path):
	today = datetime.datetime.now()
	dt = today.strftime ("%Y%m%d%H%M%S")
	copy = "./static/images/気象データ{}.png".format(dt)
	shutil.copy(path,copy)
	png_path = "/static/images/気象データ{}.png".format(dt)
	return png_path

@app.route('/download',methods=["get"])
def download():
	# export/気象データ.png
	# path = "./" + file.png_export_path("temperature_analysis")
	directory = "./export"
	file_name = "気象データ.xlsx"
	# file_name = "気象データ.xlsx"
	return send_from_directory(directory,file_name)


@app.route('/')
def hello():
    name = "Hoge"
    return redirect("/temperature")

#気象データメイン画面
@app.route('/temperature',methods=["get"])
def main_temperature():
    return render_template('main_temperature.html', title='メイン画面')

#予測のための、気象データ入力
@app.route('/temperature/pred',methods=["get"])
def input_temperature():
    return render_template('pred_temperature.html', title='flask test')

#気象データ予測結果表示
@app.route('/temperature/pred/exec',methods=["post"])
def pred_temperature():
	# データを用意
	avg_tem = float(request.form.get("avg_tem"))
	max_tem = float(request.form.get("max_tem"))
	min_tem = float(request.form.get("min_tem"))
	mag = float(request.form.get("min_tem"))
	hum = float(request.form.get("hum"))
	timing = request.form.get("timing")
	# input_values = [avg_tem,max_tem,min_tem,mag,hum,timing]
	df = logic.temperature_analysis.process_for_learning()
	#予測
	y_pred = logic.temperature_analysis.predict_temperature(df,avg_tem,max_tem,min_tem,mag,hum,timing)
	if y_pred[0] == 1:
		result = "需要あり"
	else:
		result = "需要なし"
	return result

#気象データ分析
@app.route('/temperature/analyze',methods=["get","post"])
def analyze_temperature():
	analysis_list = ["平均気温","最高気温","最低気温","最大震度","平均湿度","時期","地域"]
	if request.method == "GET":
		return render_template('analyze_temperature.html', title='気象データ分析',analysis_list=analysis_list)
	elif request.method == "POST":
		x_name = request.form.get("x_val")
		y_name = request.form.get("y_val")
		label_name = "時期"
		weather_df = logic.temperature_analysis.join_weather()
		ptrip_df =logic.temperature_analysis.get_popular_trip()
		join_df = logic.temperature_analysis.join_season(weather_df,ptrip_df)
		df_list = logic.temperature_analysis.divide_season(join_df)
		#pngファイルを作成
		path = logic.temperature_analysis.export_png(df_list,x_name,y_name,label_name)
		#pngファイルを指定ディレクトリーにコピー
		png_path = pngfile_copy(path)
		return render_template('analyze_temperature.html', title='気象データ分析',analysis_list=analysis_list,png_path=png_path)

# #予測のための、取扱金額データ入力
# @app.route('/handling_price/pred',methods=["get"])
# def input_handling_price():
#     return render_template('handling_price.html', title="取扱金額データ入力")

# #取扱金額データ予測結果表示
# @app.route('/handling_price/pred/exec',methods=["post"])
# def pred_handling_price():
# 	switch = request.form.get("switch")
# 	num = request.form.get("num")
# 	flg = logic.prediction.switch_sales(switch,num)
# 	return render_template('handling_price.html', title="取扱金額データ入力")

if __name__ == "__main__":
    app.run(port=8010, debug=True)