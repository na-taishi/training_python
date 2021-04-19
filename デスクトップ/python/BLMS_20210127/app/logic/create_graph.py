from io import BytesIO

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import japanize_matplotlib
from bokeh.plotting import figure
from bokeh.models import HoverTool,ColumnDataSource,CDSView, GroupFilter
from bokeh.embed import components

import logic
import config

#グラフ作成処理

#棒グラフ作成
def make_bar(result,title):
    label = []
    height = []
    for i in result:
        tmp = list(i)
        label.append(tmp[0])
        height.append(tmp[1])
    #figsize=(x, y)で画像のサイズを設定
    fig, ax = plt.subplots(figsize=(8.8, 6.6))
    ax.bar(label, height)
    ax.set_title(title)
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    return data

#折れ線グラフ作成
def make_plot(result,genre_list,title):
    #figsize=(x, y)で画像のサイズを設定
    fig, ax = plt.subplots(figsize=(8.8, 6.6))
    xticks =["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]
    xlabel = "貸出日"
    ylabel = "貸出数"
    #ジャンルごとにグラフ作成 
    for count,genre in enumerate(genre_list):
        label =[]
        height = []
        for row in result[count]:
            label.append(row[0])
            height.append(row[2])

        #ジャンル毎に色を設定
        for value in config.genre_conf.GENRES:
            if genre == value:
                color = config.color_conf.GENRE(genre)
        ax.plot(label, height, label=genre, c=color)
    ax.set_title(title)
    ax.set_xticklabels(xticks)
    plt.grid()
    plt.legend(loc="upper right")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    return data

#散布図作成(対話的な可視化のため、Bokehを使用)
def make_scatter(df,genre_list,title):
    #DataFrameを渡す
    source = ColumnDataSource(df)
    #データをFilterでジャンルごとに抽出
    views = []
    for genre in genre_list:
        view = CDSView(source=source, filters=[GroupFilter(column_name="genre", group=genre)])
        views.append(view)
    # グラフサイズおよびタイトルの設定
    fig = figure(plot_height=660,plot_width=880,title=title,x_axis_type="datetime")
    fig.xaxis.axis_label = "購入日"
    fig.yaxis.axis_label = "書籍総数"
    # HoverToolの設定
    hover = HoverTool(tooltips=[("タイトル","@title")])
    fig.add_tools(hover)
    # 散布図
    for count,view in enumerate(views):
        #ジャンル毎に色を設定
        for value in config.genre_conf.GENRES:
            if genre_list[count] == value:
                color = config.color_conf.GENRE(value)
        fig.circle(x="purchase_date",y="total",source=source,legend_label=genre_list[count],view=view ,color=color)
    #htmlに埋め込むデータを作成
    script, div = components(fig)
    data = [script, div]
    return data

#空のグラフ作成
def not_make():
    fig, ax = plt.subplots(figsize=(8.8, 6.6))
    ax.text(0.2,0.5,"データがありません。",fontsize=30)
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    return data