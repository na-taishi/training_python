import PySimpleGUI as sg

#実行できない
sg.theme('Dark Blue 3')
layout = []

class Screen:
	def __init__(self, sc_layout,title,size):
		# 初期化
		#オプションの設定と標準レイアウト
		sg.theme('Dark Blue 3')
		self.layout = sc_layout
		#ウィンドウの生成
		window = sg.Window(title=self.title,size=self.size).layout(layout)

	#close	
	def close(self):
		window.close()

layout = [
[sg.Text('HOME画面')],
[sg.Submit(button_text='予測',size=(10, 1))],
[sg.Submit(button_text='end')]
]
title = 'HOME画面'
size = (10, 1)
screen = Screen(layout,title,size)
win = screen.window
# イベントループ
while True:
	event, values = win.read()
	if event is None:
		print('exit')
		break
	if event == '予測':
		print("予測画面へ遷移")
		screen.close()
	elif event == 'end':
		print("終了")
		screen.close()
screen.close()
# def test():
# 	#オプションの設定と標準レイアウト
# 	sg.theme('Dark Blue 3')
# 	layout = [
# 	[sg.Text('HOME画面')],
# 	[sg.Submit(button_text='予測',size=(10, 1))],
# 	[sg.Submit(button_text='end')]
# 	]
# 	#ウィンドウの生成
# 	window = sg.Window(title='HOME画面',size=(800, 600)).layout(layout)
# 	# イベントループ
# 	while True:
# 		event, values = window.read()
# 		if event is None:
# 			print('exit')
# 			break
# 		if event == '予測':
# 			print("予測画面へ遷移")
# 			c1()
# 			window.close()
# 		elif event == 'end':
# 			print("終了")
# 			window.close()
# 	#ウィンドウの破棄と終了
# 	window.close()