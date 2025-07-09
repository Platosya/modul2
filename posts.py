from flask import Flask, render_template, request,redirect,url_for
import sqlite3
app = Flask(__name__)
connection = sqlite3.connect('db.db', check_same_thread=False)
cursor = connection.cursor()
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

if __name__ == '__main__':
    app.run()