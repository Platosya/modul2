from flask import Flask, render_template
app =Flask(__name__)
@app.route('/index/')
def index():
    return render_template('index.html')
@app.route("/")
def hello_world():
    context= {
        'posts':[{
            'title':'pineapple',
            'content':'ya riba yozh, ti riba yozh'
        },
        {
            'title': 'orange',
            'content': 'i have a 6.7 dihhhh'
        },
        {
            'title': 'apple',
            'content': 'sybau'
        }]}
    return render_template('blog.html',**context)

#@app.route('/<answer>/')
#def game(answer):
#    if answer.lower() == 'yes':
#        return 'write the number'
#    else:
#        return 'ok'

@app.route('/yes/<number>/')
def say_number(number):
    return 'u chose a number ' + number

@app.route('/Platon/')
def hello_platon():
    return 'Hi,Platon'

@app.route("/bye/#")
def bye():
    return "Pokakis"


if __name__ == '__main__':
    app.run()