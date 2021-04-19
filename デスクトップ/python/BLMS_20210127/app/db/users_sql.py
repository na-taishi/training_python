#ユーザー確認(ログイン)
check_user = "SELECT * FROM users WHERE employee_number = %s AND password = %s"

#ユーザー登録
register_user = "INSERT INTO users (employee_number,name,division,mail_address,password) VALUES(%s,%s,%s,%s,%s)"

#指定ユーザー取得
find_user = "SELECT * FROM users WHERE employee_number = %s;"

#ユーザー取得(あいまい検索)
search_number = "SELECT * FROM users WHERE CAST(employee_number AS VARCHAR) like %s AND status not in(99) ORDER BY employee_number;"
search_name = "SELECT * FROM users WHERE name like %s AND status not in(99) ORDER BY employee_number;"
search_division = "SELECT * FROM users WHERE division like %s AND status not in(99) ORDER BY employee_number;"

#使用可能ユーザー取得
available_users = "SELECT * FROM users WHERE status = 0 ORDER BY employee_number;"
#使用不能ユーザー取得
unusable_users = "SELECT * FROM users WHERE status = 1 ORDER BY employee_number;"

#全ユーザー取得(管理用除く)
find_user_all = "SELECT * FROM users WHERE status NOT IN(99) ORDER BY employee_number;"

#ステータス変更
update_status = "UPDATE users SET(updated_at,status) = (%s,%s) WHERE employee_number = %s;"

#ユーザー情報変更
update_user = "UPDATE users SET(employee_number,name,division,mail_address,password,updated_at,status) = (%s,%s,%s,%s,%s,%s,%s) WHERE employee_number = %s;"

#ユーザー削除
delete_user = "DELETE FROM users WHERE employee_number = %s;"