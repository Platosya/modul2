from flask import Flask, render_template, request,redirect,url_for
import sqlite3

from werkzeug.security import generate_password_hash

app = Flask(__name__)
connection = sqlite3.connect('db.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
 );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  user_id INTEGER
  )''')

connection.commit()
def close_db(connection=None):
    if connection is not None:
        connection.close()
@app.teardown_appcontext
def close_connection (exception):
    close_db()
@app.route("/")
def index():
    cursor.execute('SELECT * from post')
    result = cursor.fetchall()
    posts = []
    for post in reversed(result):
        posts.append(
            {'id':post[0],'title':post[1],'content': post[2]}
        )
    context = {'posts': posts}
    return render_template('blog.html', **context)
@app.route('/add/',methods=['GET','POST'])
def add_post():
    if request.method =="POST":
        title = request.form['title']
        content = request.form['content']
        cursor.execute(
            'INSERT INTO post (title, content) VALUES(?,?)',
            (title,content)
        )
        connection.commit()
        return redirect (url_for('index'))
    return render_template('addpost.html')
@app.route('/post/<post_id>')
def post(post_id):
    result = cursor.execute(
        'SELECT (id,title,content) FROM post WHERE id=?',(post_id,)
    ).fetchone()
    post_dict={'id':result[0],'title':result[1],'content':result[2]}
    return render_template('post.html',post=post_dict)
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            cursor.execute('INSERT INTO user (username password_hash)VALUES(?,?)',
                           (username, generate_password_hash(password,
                                                            method='pbkdf2:sha256'))
                           )
            connection.commit()
            print('Ur connection has been made sucesfully')
        except sqlite3.IntegrityError:
            return render_template('register.html',
                                   message= 'Username already exists!')
    return render_template('register.html')


if __name__ == '__main__':
    app.run()