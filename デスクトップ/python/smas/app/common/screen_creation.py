import PySimpleGUI as sg

import logic

# ##画面作成##

def create_screen():
	#オプションの設定と標準レイアウト
	sg.theme('Dark Blue 3')
	layout = [
	[sg.Text('Python GUI')],
	[sg.Text('', size=(15, 1)), sg.InputText()],
	[sg.Radio('取扱額', "RADIO1", default=True),sg.Radio('取扱人数（人）', "RADIO1")],
	[sg.Submit(button_text='実行ボタン')]
	]
	#ウィンドウの生成
	window = sg.Window('取扱金額予測', layout)
	# イベントループ
	while True:
		event, values = window.read()
		if event is None:
			print('exit')
			break
		if event == '実行ボタン':
			if not values[0]:
				continue
			elif not values[0].isdecimal():
				show_message = "数値を入力してください!"
				sg.popup(show_message)
				continue

			show_message =  values[0] + 'が入力されました。\n'
			if values[1] == True:
				target = "取扱額"
				show_message +=  target + 'が選択されました。\n'
			else:
				target = "取扱人数（人）"
				show_message +=  target + 'が選択されました。\n'
			print(show_message)
			#エクセル出力
			flg = logic.prediction.switch_sales(target,int(values[0]))
			#ポップアップ
			if flg == True:
				show_message = "出力完了!"
			else:
				show_message
			sg.popup(show_message)
	#ウィンドウの破棄と終了
	window.close()

#取扱金額予測
def handling_price_screen():
	#取扱人数（人）
	h_num = "ninzu"
	#取扱額
	h_pr = "kingaku"
	#実行ボタン
	bt_execution = "execution"
	#出力完了
	msg_finish = "出力完了!"

	#オプションの設定と標準レイアウト
	sg.theme('Dark Blue 3')
	layout = [
	[sg.Text('Python GUI')],
	[sg.Text('', size=(15, 1)), sg.InputText()],
	[sg.Radio(h_pr, "RADIO1", default=True),sg.Radio(h_num, "RADIO1")],
	[sg.Submit(button_text=bt_execution)]
	]
	#ウィンドウの生成
	window = sg.Window('取扱金額予測', layout)
	# イベントループ
	while True:
		event, values = window.read()
		if event is None:
			print('exit')
			break
		if event == bt_execution:
			if not values[0]:
				continue
			elif not values[0].isdecimal():
				show_message = "数値を入力してください!"
				sg.popup(show_message)
				continue

			show_message =  values[0] + 'が入力されました。\n'
			if values[1] == True:
				target = "取扱額"
				show_message +=  target + 'が選択されました。\n'
			else:
				target = "取扱人数（人）"
				show_message +=  target + 'が選択されました。\n'
			print(show_message)
			#エクセル出力
			flg = logic.prediction.switch_sales(target,int(values[0]))
			#ポップアップ
			if flg == True:
				show_message = msg_finish
			else:
				show_message
			sg.popup(show_message)
	#ウィンドウの破棄と終了
	window.close()