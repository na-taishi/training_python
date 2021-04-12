import re

import requests
from bs4 import BeautifulSoup

##スクレイピング##


#リストを指定した要素数ごとに分ける
def split_list(txt_list,num):
	start = 0
	rows = []
	for i in txt_list:
		rows.append(txt_list[start:start+num])
		start += num
		if start >= len(txt_list):
			break
	return rows

#指定classをスクレイピング
def get_class(url,class_name,split_str,num):
	#サイトからデータを取得
	res = requests.get(url)
	#データ抽出
	bs = BeautifulSoup(res.content, "html.parser")
	elems = bs.find(class_=class_name)
	#タグ削除と分割
	txt_list = re.split(split_str,elems.text)
	#空の要素を削除
	txt_remove = [i for i in txt_list if i != '']
	#一定要素で分ける
	rows = split_list(txt_remove, num)
	return rows


#指定classをスクレイピング
def get_class_all(url,class_name,split_str):
	#サイトからデータを取得
	res = requests.get(url)
	#データ抽出
	bs = BeautifulSoup(res.content, "html.parser")
	elems = bs.find_all(class_=class_name)
	rows =[]
	for i in elems:
		#タグと空白削除
		txt = i.text.strip()
		#分割
		row = re.split(split_str,txt)
		rows.append((row))
	return rows