from flask import Flask,render_template,request,redirect,session,url_for,make_response
import logic
import datetime
import config

#Flaskオブジェクトの生成
app = Flask(__name__)

app.secret_key = "aaa"

#閲覧制御
def check_session(status):
    return_data = render_template("session_err.html",css="",title="エラー")
    #ログインしていない状態の場合はエラー
    if not session.get("user_id"):
        return return_data
    else:
        #管理者用ページは99、一般ユーザーページは0
        if status == 99:
            user_status = session.get("user_status")
            #ログインしたアカウントが管理者以外のときはエラー
            if not user_status == 99:
                return return_data
        elif status == 0:
            user_status = session.get("user_status")
            #ログインしたアカウントが一般以外のときはエラー
            if not user_status == 0:
                return return_data
            
@app.route("/")
def top():
    return redirect("/login")

#ログイン処理
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        msg = request.args.get("msg")
        if not msg:
            #msgにNoneが入っているときにNoneと表示させない
            msg = ""
        return render_template("login.html",css="static/css/layout.css",title="ログイン",msg=msg)
    elif request.method == 'POST':
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        result = logic.login.check_user(user_id,password)
        #対象ユーザーがテーブルに存在するかの確認
        if result:
            session["user_id"] = result[1]
            session["user_name"] = result[2]
            status = result[8]
            session["user_status"] = status
            #ユーザーステータス確認(0：使用可能、1：使用不可、99：管理用)
            if status == 99:
                return redirect("/user_list")
            elif status == 0:
                return redirect("/borrowed_list")
            else:
                session.pop("user_id", None)
                session.pop("user_name", None)
                msg = "ログインに失敗しました。"
                return redirect(url_for("login",msg=msg))
        else:
            msg = "ログインに失敗しました。"
            return redirect(url_for("login",msg=msg))

#ログアウト処理
@app.route("/logout",methods=['GET'])
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("user_status", None)
    session.pop("books", None)
    return redirect("/login")

#ユーザー登録
@app.route("/user_registration",methods=['GET','POST'])
def user_registration():
    if request.method == 'GET':
        divishons = config.division_conf.DIVISIONS
        return render_template("/user_registration.html",css="static/css/layout.css",title="ユーザー登録",divishons=divishons)
    else:
        employee_number = request.form.get("employee_number")
        name = request.form.get("name")
        division = request.form.get("division")
        mail_address = request.form.get("mail_address")
        password = request.form.get("password")
        values = {"employee_number":employee_number,"name":name,"division":division,"mail_address":mail_address,"password":password}
        session["values"] = values
        bt_transition = "/check_user_registration"
        transition_name = "登録"
        bt_return = "/login"

        return render_template("/confirmation.html",css="",title="ユーザー登録確認",msg="登録してもよろしいでしょうか。",bt_transition=bt_transition,transition_name=transition_name,bt_return=bt_return)

#ユーザー登録確認
@app.route("/check_user_registration",methods=['GET','POST'])
def check_user_registration():
    values = session.get("values")
    session.pop("values", None)
    #登録
    flg = logic.login.register_user(values["employee_number"],values["name"],values["division"],values["mail_address"],values["password"])
    bt_transition = "/login"
    transition_name = "ログイン画面へ戻る"
    if flg == 0:
        msg = "ユーザーの登録が完了しました。"
        title = "完了"
    else:
        msg = "すでに登録されている社員番号です。"
        title = "登録エラー"
    return render_template("/completion.html",css="",title=title,msg=msg,bt_transition=bt_transition,transition_name=transition_name)


#借用一覧
@app.route("/borrowed_list",methods=['GET','POST'])
def borrowed_list():
    #ログイン状態の確認
    session_flg = check_session(0)
    if session_flg:
        return session_flg
    
    user_id = session.get("user_id")
    #借用書籍一覧取得
    values = logic.borrowed_list.get_borrower_list(user_id)
    name = session.get("user_name")
    return render_template("/borrowed_list.html",css="",title="借用一覧" ,values=values,name=name)

#返却
@app.route("/return_book",methods=['GET','POST'])
def return_book():
    books = request.form.getlist("check")
    if not books:
        #チェックが何もされていない状態のボタン押下
        return redirect("/borrowed_list")
    else:
        session["borrowed"] = books
        bt_transition = "/check_reurn"
        transition_name = "返却"
        bt_return = "/borrowed_list"
        return render_template("/confirmation.html",css="",title="返却確認",msg="本を返しますか。",bt_transition=bt_transition,transition_name=transition_name,bt_return=bt_return)

#返却確認
@app.route("/check_reurn",methods=['GET','POST'])
def check_reurn():
    borrower = session.get("user_id")
    books = session.get("borrowed")
    stock = 1
    
    for book_id in books:
        #返却
        logic.borrowed_list.return_borrowed(book_id,borrower,stock)
    
    session.pop("borrowed", None)
    bt_transition = "/borrowed_list"
    transition_name = "返却画面"
    return render_template("/completion.html",css="",title="完了",msg="返却処理が完了しました。",bt_transition=bt_transition,transition_name=transition_name)

#書籍一覧
@app.route("/book_list",methods=['GET','POST'])
def book_list():
    #閲覧制御
    session_flg = check_session(0)
    if session_flg:
        return session_flg
    
    borrower = session.get("user_id")
    #書籍一覧取得
    result = logic.book_list.get_book_list(borrower)
    #チェックボックスの非活性化
    books = []
    books = session.get("books")
    values = logic.book_list.change_disabled(result,books)
    name = session.get("user_name")
    return render_template("/book_list.html",css="",title="書籍一覧" ,values=values,name=name)

#書籍検索
@app.route("/search_books",methods=['GET','POST'])
def search_books():
    search = request.args.get("search")
    selection = request.args.get("selection")
    borrower = session.get("user_id")
    #書籍一覧取得
    result = logic.book_list.get_books_search(search,selection,borrower)
    #チェックボックスの非活性化
    books = []
    books = session.get("books")
    values = logic.book_list.change_disabled(result,books)
    name = session.get("user_name")
    return render_template("/book_list.html",css="",title="書籍一覧" ,values=values,name=name)

#書籍登録
@app.route("/book_registration",methods=['GET','POST'])
def book_registration():
    if request.method == 'GET':
        buyer = session.get("user_name")
        date = datetime.datetime.today()
        genres = config.genre_conf.GENRES
        return render_template("/book_registration.html",css="static/css/layout.css",title="書籍登録",buyer=buyer,date=date,genres=genres)
    else:
        title = request.form.get("title")
        author = request.form.get("author")
        publisher = request.form.get("publisher")
        price = request.form.get("price")
        buyer = request.form.get("buyer")
        purchase_date = request.form.get("purchase_date")
        total = request.form.get("total")
        genre = request.form.get("genre")
        values = {"title":title,"author":author,"publisher":publisher,"price":price,"buyer":buyer,"purchase_date":purchase_date,"total":total,"genre":genre}
        session["values"] = values
        bt_transition = "/check_book_registration"
        transition_name = "登録"
        bt_return = "/book_list"

        return render_template("/confirmation.html",css="",title="書籍登録確認",msg="登録してもよろしいでしょうか。",bt_transition=bt_transition,transition_name=transition_name,bt_return=bt_return)

#書籍登録確認
@app.route("/check_book_registration",methods=['GET','POST'])
def check_book_registration():
    values = session.get("values")
    session.pop("values", None)
    #登録
    logic.book_list.register_book(values["title"],values["author"],values["publisher"],values["price"],values["buyer"],values["purchase_date"],values["total"],values["genre"])
    bt_transition = "/book_list"
    transition_name = "書籍一覧画面へ戻る"
    return render_template("/completion.html",css="",title="完了",msg="書籍の登録が完了しました。",bt_transition=bt_transition,transition_name=transition_name)

#カート
@app.route("/cart",methods=['GET','POST'])
def cart():
    #閲覧制御
    session_flg = check_session(0)
    if session_flg:
        return session_flg
    
    books = session.get("books")
    #カートに入れた書籍を取得
    values = logic.cart.get_book_cart(books)
    name = session.get("user_name")
    #翌月取得(%Y-%m-%d)
    date = logic.datetime_format.get_n_month(1,"day")
    return render_template("/cart.html",css="",title="カート" ,values=values,name=name,date=date)

#カート追加
@app.route("/add_cart",methods=['GET','POST'])
def add_cart():
    #詳細画面と書籍一覧画面の判定
    book_id = request.form.get("book_id")
    if book_id:
        books = [book_id]
    else:
        books = request.form.getlist("check")
    tmp = session.get("books")
    if tmp:
        books += tmp
        
    session["books"] = books
    return redirect("/cart")

#カート削除
@app.route("/delete_cart",methods=['GET','POST'])
def delete_cart():
    books = session.get("books")
    del_books = request.form.get("book_id")
    books.remove(del_books)
    session["books"] = books
    return redirect("/cart")

#借用
@app.route("/borrow_book",methods=['GET','POST'])
def borrow_book():    
    if not session.get("books"):
        return redirect("/book_list")
    else:
        session["date"] = request.form.getlist("date")
        bt_transition = "/check_borrowed"
        transition_name = "借用"
        bt_return = "/cart"
        return render_template("/confirmation.html",css="",title="借用確認",msg="本を借りますか。",bt_transition=bt_transition,transition_name=transition_name,bt_return=bt_return)

#借用確認
@app.route("/check_borrowed",methods=['GET','POST'])
def check_borrowed():
    borrower = session.get("user_id")
    values = session.get("date")
    stock = 1
    books = session.get("books")
    count = 0
    for book_id in books:
        expected_return_date = values[count]
        #借用
        logic.cart.borrow(borrower,expected_return_date,stock,book_id)
        count += 1
    
    session.pop("books", None)
    bt_transition = "/borrowed_list"
    transition_name = "借用一覧画面"
    return render_template("/completion.html",css="",title="完了",msg="借用処理が完了しました。",bt_transition=bt_transition,transition_name=transition_name)

#詳細
@app.route("/book_detail",methods=['GET','POST'])
def book_detail():
    #書籍取得
    book_id = request.args.get("book_id")
    values = logic.book_detail.get_book_detail(book_id)
    #戻る画面のデータ取得
    title = request.args.get("return_screen")
    bt_return = logic.book_detail.return_screen(title)
    #カート追加ボタンの非活性化
    books = []
    books = session.get("books")
    disabled = logic.book_detail.change_disabled(title,values[8],books,book_id)
    return render_template("/book_detail.html",css="static/css/layout.css",title="詳細" ,values=values,bt_return=bt_return,disabled=disabled)

#書籍更新
@app.route("/book_edit",methods=['GET','POST'])
def book_edit():
    if request.method == 'GET':
        #初期値の取得
        values = session.get("values")
        session.pop("values", None)
        if not values:
            book_id = request.args.get("book_id")
            title = request.args.get("title")
            author = request.args.get("author")
            publisher = request.args.get("publisher")
            price = request.args.get("price")
            buyer = request.args.get("buyer")
            purchase_date = request.args.get("purchase_date")
            total = request.args.get("total")
            genre = request.args.get("genre")
            genres = config.genre_conf.GENRES
            values = {"book_id":book_id,"title":title,"author":author,"publisher":publisher,"price":price,"buyer":buyer,"purchase_date":purchase_date,"total":total,"genre":genre}
        return render_template("/book_edit.html",css="static/css/layout.css",title="編集",values=values,genres=genres)
    else:
        #更新する値をセッションに保存
        book_id = request.form.get("book_id")
        title = request.form.get("title")
        author = request.form.get("author")
        publisher = request.form.get("publisher")
        price = request.form.get("price")
        buyer = request.form.get("buyer")
        purchase_date = request.form.get("purchase_date")
        total = request.form.get("total")
        genre = request.form.get("genre")
        values = {"book_id":book_id,"title":title,"author":author,"publisher":publisher,"price":price,"buyer":buyer,"purchase_date":purchase_date,"total":total,"genre":genre}
        session["values"] = values
        bt_transition = "/check_book_edit"
        transition_name = "更新"
        bt_return = "/book_edit"

        return render_template("/confirmation.html",css="",title="書籍更新確認",msg="更新してもよろしいでしょうか。",bt_transition=bt_transition,transition_name=transition_name,bt_return=bt_return)

#書籍更新確認
@app.route("/check_book_edit",methods=['GET','POST'])
def check_book_edit():
    values = session.get("values")
    session.pop("values", None)
    #登録
    logic.book_detail.update_book(values["book_id"],values["title"],values["author"],values["publisher"],values["price"],values["buyer"],values["purchase_date"],values["total"],values["genre"])
    bt_transition = "/book_list"
    transition_name = "書籍一覧画面へ戻る"
    return render_template("/completion.html",css="",title="完了",msg="書籍の更新が完了しました。",bt_transition=bt_transition,transition_name=transition_name)

#書籍削除
@app.route("/delete_book",methods=['POST'])
def delete_book():
    book_id = request.form.get("book_id")
    session["book_id"] = book_id
    
    bt_transition = "/check_delete_book"
    transition_name = "削除"
    bt_return = "/book_list"

    return render_template("/confirmation.html",css="",title="書籍削除確認",msg="削除してもよろしいでしょうか。",bt_transition=bt_transition,transition_name=transition_name,bt_return=bt_return)

#書籍削除確認
@app.route("/check_delete_book",methods=['POST'])
def check_delete_book():
    book_id = session.get("book_id")
    session.pop("book_id", None)
    #削除
    logic.book_detail.delete_book(book_id)
    bt_transition = "/book_list"
    transition_name = "書籍一覧画面へ戻る"
    return render_template("/completion.html",css="",title="完了",msg="書籍の削除が完了しました。",bt_transition=bt_transition,transition_name=transition_name)

#管理者画面
@app.route("/user_list",methods=['GET'])
def user_list():
    #ログイン状態の確認
    session_flg = check_session(99)
    if session_flg:
        return session_flg

    #ユーザー一覧取得
    values = logic.management.get_user_list()
    return render_template("/management.html",css="",title="管理者",values=values)

#ステータス変更
@app.route("/change_status",methods=['POST'])
def change_status():
    employee_number = request.form.get("employee_number")
    status = request.form.get("status")
    #ユーザーのステータス変更(0は使用可能、1は使用不可)
    logic.management.update_status(employee_number,status)
    return redirect("/user_list")

#ユーザー情報変更
@app.route("/user_edit",methods=['GET','POST'])
def user_edit():
    if request.method == 'GET':
        employee_number = request.args.get("employee_number")
        name = request.args.get("name")
        division = request.args.get("division")
        mail_address = request.args.get("mail_address")
        password = request.args.get("password")
        status = request.args.get("status")
        values = (employee_number,name,division,mail_address,password,status)
        divishons = config.division_conf.DIVISIONS
        return render_template("/user_edit.html",css="static/css/layout.css",title="ユーザー編集",values=values,divishons=divishons)
    else:
        #更新する値をセッションに保存
        employee_number = request.form.get("employee_number")
        name = request.form.get("name")
        division = request.form.get("division")
        mail_address = request.form.get("mail_address")
        password = request.form.get("password")
        status = request.form.get("status")
        values = {"employee_number":employee_number,"name":name,"division":division,"mail_address":mail_address,"password":password,"status":status}
        session["values"] = values
        bt_transition = "/check_user_edit"
        transition_name = "更新"
        bt_return = "/user_edit"

        return render_template("/confirmation.html",css="",title="ユーザー更新確認",msg="更新してもよろしいでしょうか。",bt_transition=bt_transition,transition_name=transition_name,bt_return=bt_return)

#ユーザー情報変更確認
@app.route("/check_user_edit",methods=['POST'])
def check_user_edit():
    values = session.get("values")
    session.pop("values", None)
    #更新
    logic.management.update_user(values["employee_number"],values["name"],values["division"],values["mail_address"],values["password"],values["status"])
    bt_transition = "/user_list"
    transition_name = "ユーザ一覧画面へ戻る"
    return render_template("/completion.html",css="",title="完了",msg="ユーザーの更新が完了しました。",bt_transition=bt_transition,transition_name=transition_name)

#ユーザー削除
@app.route("/delete_user",methods=['POST'])
def delete_user():
    employee_number = request.form.get("employee_number")
    session["employee_number"] = employee_number
    
    bt_transition = "/check_delete_user"
    transition_name = "削除"
    bt_return = "/user_list"

    return render_template("/confirmation.html",css="",title="ユーザー削除確認",msg="削除してもよろしいでしょうか。",bt_transition=bt_transition,transition_name=transition_name,bt_return=bt_return)

#ユーザー削除確認
@app.route("/check_delete_user",methods=['POST'])
def check_delete_user():
    employee_number = session.get("employee_number")
    session.pop("employee_number", None)
    #削除
    logic.management.delete_user(employee_number)
    bt_transition = "/user_list"
    transition_name = "ユーザー一覧画面へ戻る"
    return render_template("/completion.html",css="",title="完了",msg="ユーザーの削除が完了しました。",bt_transition=bt_transition,transition_name=transition_name)

#ユーザー検索
@app.route("/search_users",methods=['GET','POST'])
def search_users():
    search = request.args.get("search")
    selection = request.args.get("selection")
    #ユーザー一覧取得
    values = logic.management.get_users_search(search,selection)
    name = session.get("user_name")
    return render_template("/management.html",css="",title="ユーザー一覧" ,values=values,name=name)

#グラフ表示
@app.route("/graph_creation")
def graph_creation():
    select_list = ["selection01","selection02","selection03","selection04","selection05"]
    graph_list = ["genre_all.png","genre_month.png","genre_year.png","no_graph_data.png","monthly_genre_count.png"]
    name_list = ["貸出回数(ジャンル別)","貸出回数(月間ジャンル別)","貸出回数(年間ジャンル別)","長期間の貸出がない書籍","ジャンル別各月総数"]
    num = len(select_list)
    values = not_borrow()
    if values:
        text_css = values[2]
        text_script = values[3]
    else:
        text_css=""
        text_script=""
    return render_template("/graph_creation.html",css="",title="グラフ作成",num=num,select_list=select_list,graph_list=graph_list,name_list =name_list,values=values,text_css=text_css,text_script=text_script)


#貸出回数(ジャンル別)グラフ作成
@app.route("/genre_all.png")
def genre_all():
    data = logic.analysis.get_genre("all")
    if data == False:
        return redirect("/no_graph_data.png")
    return data

#貸出回数(月間ジャンル別)グラフ作成
@app.route("/genre_month.png")
def genre_month():
    data = logic.analysis.get_genre("month")
    if data == False:
        return redirect("/no_graph_data.png")
    return data

#貸出回数(年間ジャンル別)グラフ作成
@app.route("/genre_year.png")
def genre_year():
    data = logic.analysis.get_genre("year")
    if data == False:
        return redirect("/no_graph_data.png")
    return data

#長期間の貸出がない書籍グラフ作成
@app.route("/not_borrow")
def not_borrow():
    #グラフ作成とhtmlに埋め込むJavaScriptとdivの生成
    data = logic.analysis.not_borrow_long_period()
    if data == False:
        values = data
    else:
        script, div = data[0],data[1]
        #Bokehを使用するためにhtmlのヘッダーに埋め込む
        text_css = ["https://cdn.pydata.org/bokeh/release/bokeh-2.2.3.min.css"]
        text_script = ["https://cdn.pydata.org/bokeh/release/bokeh-2.2.3.min.js"]
        values = [script,div,text_css,text_script]
    return values

#ジャンル別に各月の総数グラフ作成
@app.route("/monthly_genre_count.png")
def monthly_genre_count():
    #去年(%Y-%m-%d)
    specified_year = logic.datetime_format.get_n_year(-1,"year")
    data = logic.analysis.create_monthly_genre_count(specified_year)
    if data == False:
        return redirect("/no_graph_data.png")
    return data

#グラフ作成するためのデータがない時の処理
@app.route("/no_graph_data.png")
def no_graph_data():
    data = logic.create_graph.not_make()
    return data

if __name__ == "__main__":
    app.run(debug=True)