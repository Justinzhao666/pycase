# encoding=utf-8
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

'''
加载配置文件,用环境变量重写配置
secret_key 是保证客户端会话的安全的要点。正确选择一个尽可能难猜测、尽可能复杂的密钥。
调试标志关系交互式调试器的开启。 永远不要在生产系统中激活调试模式 ，因为它将允许用户在服务器上执行代码。
'''
app = Flask(__name__)       # 单一的模块创建实例
app.config.update(dict(
    DATABASE=os.path.join(app.root_path + '/config/data', 'db_engine.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

'''
加载一个单独的、环境特定的配置文件是个好主意。Flask 允许你导入多份配置，并且使用最后的导入中定义的设置
只需设置一个名为 xx_SETTINGS 的环境变量，指向要加载的配置文件。
启用静默模式告诉 Flask 在没有设置该环境变量的情况下噤声
'''
app.config.from_envvar('DB_SETTINGS', silent=True)


def connect_db():
    '''Connects to the specific databse.'''
    rv = sqlite3.connect(app.config['DATABASE'])    # 建立连接
    rv.row_factory = sqlite3.Row    # 用 sqlite3.Row 表示数据库中的行。这使得可以通过字典而不是元组的形式访问行:
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
        current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('config/db_engine.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    '''Create the databse tables'''
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT title, text FROM entries ORDER BY id DESC ')
    entries = cur.fetchall()
    return render_template("show_entries.html", entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO entries (title,text) VALUES (?,?)', [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted!')
    return redirect(url_for("show_entries"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()

