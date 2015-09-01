from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    resp = make_response(render_template('hello.html', name=name))
    # if name:
    #     resp.set_cookie('username',name)
    # else:
    #     name = request.cookies.get('username')
    # resp = make_response(render_template('hello.html', name=name))
    return resp
    # return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')