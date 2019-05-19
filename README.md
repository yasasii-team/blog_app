# blog_app

やさしい会によるPythonの簡易的なブログアプリ

# Env

開発環境は主に以下になります。

```
Python 3.7
Flask 1.0.2
```

## install

このプロジェクトに必要なパッケージのインストール

```
$ pip install -r requirements.txt
```
# setting

DBの初期化などを行います

### configファイルの設定

まずはconfig.py.orgをコピーしてconfig.pyを作成します。

```
$ cd blog_app
$ cp config.py.org config.py
```

config.pyの中身を以下のように書き換えてください。
基本的には以下2つの変数の名称を各自で決めてもかまいませんが、
`DATABASE`は、開発メンバーで話を合わせるためにも、`blog_app.db`にしてください。
`SECRET_KEY`は好きなのにしても構いませんが、迷った場合は以下にしてみてください。

```
DATABASE="blog_app.db"
SECRET_KEY = "secret_01"
```
### DBの初期化

上のconfig.pyの設定が終わったら、もう一度上のディレクトリまで戻り、以下のコマンドを実行してください。

```
$ python dbinit.py
```

上記コマンドの実行後に、以下のように`blog_app.db`というファイルができていれば成功です。

```
$ ls

README.md  blog_app.db  manage.py
blog_app/  dbinit.py    requirements.txt
```

# Run

以下のコマンドででWEBアプリケーションを実行です。
もし起動時にエラーが出る場合は、上記の`setting`を終わらせてください。

```
$ python manage.py
```
