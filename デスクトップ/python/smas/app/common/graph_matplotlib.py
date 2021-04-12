import numpy as np
from matplotlib import pyplot as plt
import japanize_matplotlib

from config.color_conf import COLOR as COLOR


#散布図
def create_scatter(df_list,x_name,y_name,label_name):
	fig = plt.figure(figsize=(12, 12))
	ax = fig.add_subplot(111)
	for count,df in enumerate(df_list):
		color = COLOR(count)
		ax.scatter(df[x_name],df[y_name],color=color,label=df.iat[0,df.columns.get_loc(label_name)])
	ax.legend(bbox_to_anchor=(1.1, 1.15))
	ax.grid()
	ax.set_xlabel(x_name)
	ax.set_ylabel(y_name)
	plt.show()
	# fig.savefig('figure.png')
	return fig

#png出力
def output_png(fig,path):
	fig.savefig(path)