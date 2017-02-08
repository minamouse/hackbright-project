from flask import Flask, render_template, redirect
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/profile')
def profile():

    return render_template('profile.html')


@app.route('/logout')
def logout():

    return redirect('index.html')

if __name__ == '__main__':

    app.debug = True
    app.run(port=5000, host='0.0.0.0')
