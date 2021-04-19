import datetime
from dateutil.relativedelta import relativedelta

#tupleの日付をyyyy-mm-ddに変更(引数はタプル名と変更するインデックス)
def change_tuple(values,i):
    if not values:
        result = values
    elif not values[i]:
        result = values
    else:
        li = list(values)
        li[i] = li[i].strftime("%Y-%m-%d")
        result = tuple(li)

    return result
    
#更新時間取得("%Y-%m-%d %H:%M:%S")
def get_current_time():
    result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return result

#n月
def get_n_month(num,format):
    today = datetime.datetime.today()
    month  = today + relativedelta(months=num)
    if format == "day":
        result = month.strftime('%Y-%m-%d')
    elif format == "month":
        result = month.strftime('%Y-%m')
    return result

#n年
def get_n_year(num,format):
    today = datetime.datetime.today()
    year  = today + relativedelta(years=num)
    if format == "day":
        result = year.strftime('%Y-%m-%d')
    elif format == "month":
        result = year.strftime('%Y-%m')
    elif format == "year":
        result = year.strftime('%Y')
    return result
    