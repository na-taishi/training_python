import os
import zipfile
import itertools

#パス取得
def get_path(dirname,filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir,dirname)
    path = os.path.join(target_dir,filename) if filename else target_dir
    return path

#文字の生成処理
def generate_characters():
    #Unicode数値作成
    unicode_nums = list(range(48,58))
    #Unicodeアルファベット小文字作成
    unicode_low_al = list(range(97,123))
    #Unicodeアルファベット大文字作成
    unicode_up_al = list(range(65,90))
    #文字作成
    chr_list = unicode_nums + unicode_low_al + unicode_up_al
    chars = []
    for i in chr_list:
        str = chr(i)
        chars.append(str)
    return chars

#zipの解凍処理
def open_zip(zip_path,unzip_path,pwd):
    flg = False
    with zipfile.ZipFile(zip_path,"r") as zip_file:
        try:
            #zipの解凍
            zip_file.extractall(path=unzip_path,pwd=pwd.encode())
            print("zipファイルを解凍しました。")
            flg = True
        except RuntimeError:
            pass
        except Exception:
            pass
    return flg

#タプルの数だけ入力するパスワードを作成する処理
def generate_password(rows,num,zip_path,unzip_path):
    for row in rows:
        #パスワード作成
        pwd = ''.join(map(str,row))
        print(pwd)
        #作成したパスワードを入力
        flg = open_zip(zip_path,unzip_path,pwd)
        #解凍できたら処理を終了する
        if flg == True:
            print(pwd)
            break
    if flg == False:
        pwd = str(flg)
    return pwd

#各桁数毎にパスワードを作成して解凍する処理(1桁から指定桁数)
def digits_loop(chars,num,zip_path,unzip_path):
    for i in range(1, num+1):
        tuple_list = list(itertools.product(chars, repeat=i))
        pwd = generate_password(tuple_list,num,zip_path,unzip_path)
        if pwd != "False":
            break
    return pwd

#メイン処理
def main():
    #zipファイルのパス設定
    zip_filename = "sample.zip"
    zip_dirname = "import"
    input_path =get_path(zip_dirname,zip_filename)
    #解凍先パス設定
    output_dirname = "export"
    output_path =get_path(output_dirname,"")
    #文字作成
    chars = generate_characters()
    #桁数の設定
    num = 4
    #解凍処理
    print("解凍処理を始めます。")
    pwd = digits_loop(chars,num,input_path,output_path)
    print("PASSWORD:" + pwd)
    print("解凍処理が終了しました。")
    
    

if __name__ == "__main__":
    main()