import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,LinearAxis, Range1d
from bokeh.io import export_png

import config
from config.color_conf import COLOR as COLOR

##グラフ作成##


#PNG
def generate_png(fig,png_path):
	export_png(fig,filename=png_path)

#棒グラフ
def create_bar(df,title,x,y):
	#DataFrameを渡す
	source = ColumnDataSource(df)
	#グラフ全体の設定を行う
	fig = figure(x_range=df[x].values,plot_width=880, plot_height=660, title=title)
	#グラフ作成
	fig.vbar(x=x,width=0.5,bottom=0,top=y,color="#CAB2D6",source=source)
	return fig

#折れ線グラフ
def create_line(df_list,title,x,y1,y2,legend_list1,legend_list2,y2_min,y2_max,axis):
	#グラフ全体の設定を行う
	fig = figure(plot_width=1000, plot_height=660, title=title)
	fig.xaxis.axis_label = axis[0]
	fig.yaxis.axis_label = axis[1]
	#グラフ作成
	for count,df in enumerate(df_list):
		#DataFrameを渡す
		source = ColumnDataSource(df)
		#グラフ作成
		fig.line(x=x,line_width=5,line_alpha=0.5,y=y1,line_color=COLOR(count),source=source,legend_label=legend_list1[count])
		fig.circle(x, y1, fill_color="white", size=8,source=source)
		#y軸が2種類のとき
		if y2:
			fig.extra_y_ranges = {"y2": Range1d(start=y2_min*0.8, end=y2_max*1.2)}
			fig.line(x=x,line_width=5,line_alpha=0.5,y=y2,line_color=COLOR(count+10),source=source,y_range_name="y2",legend_label=legend_list2[count])
			fig.circle(x, y2, fill_color="white", size=8,source=source,y_range_name="y2")
			fig.add_layout(LinearAxis(y_range_name="y2", axis_label=axis[2]), 'right')
	fig.add_layout(fig.legend[0], "right") 
	fig.toolbar.logo = None
	fig.toolbar_location = None
	return fig

#散布図
def create_scatter(df_list,title,x,y,legend_list,axis):
	#グラフ全体の設定を行う
	fig = figure(plot_width=1000, plot_height=660, title=title)
	fig.xaxis.axis_label = axis[0]
	fig.yaxis.axis_label = axis[1]
	#グラフ作成
	for count,df in enumerate(df_list):
		#DataFrameを渡す
		source = ColumnDataSource(df)
		#グラフ作成
		fig.circle(x=x, y=y, fill_alpha=0.5,line_color=COLOR(count),fill_color=COLOR(count), size=8,source=source,legend_label=legend_list[count])
	fig.add_layout(fig.legend[0], "right") 
	fig.toolbar.logo = None
	fig.toolbar_location = None
	return fig

#線の追加
def add_line(fig,x,y,add_color,add_legend,is_circle):
	if not add_color:
		add_color = COLOR(10)	
	#グラフ作成
	fig.line(x,y,line_width=5,line_alpha=0.5,line_color=add_color,legend_label=add_legend)
	if is_circle == True:
		fig.circle(x, y, fill_color="white", size=8)
	return fig
