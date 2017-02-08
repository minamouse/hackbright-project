from flask import Flask, render_template, redirect, request, jsonify
import os
from parse_music import sample_song

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


@app.route('/process_song', methods=['POST'])
def song():

    melody = request.form.get('melody')
    sample_song(melody)
    return jsonify({})


if __name__ == '__main__':

    app.debug = True
    app.jinja_env.auto_reload = True
    app.run(port=5000, host='0.0.0.0')
