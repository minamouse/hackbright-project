from flask import Flask, render_template, redirect, request, jsonify, session, flash
import os
from parse_music import sample_song
from model import User, Song, db, connect_to_db

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def process_login():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
        if user.password != password:
            flash('Incorrect password!')
            return redirect('/')
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    session['user'] = user.username

    return redirect('/')


@app.route('/save', methods=['POST'])
def save_song():

    if 'user' not in session:
        flash('Please log in to save your songs!')
        return redirect('/')

    name = request.form.get('name')
    user = User.query.filter_by(username=session['user']).first()
    try:
        song = Song.query.order_by('song_id desc').limit(1).one()
        song_id = song.song_id
    except:
        song_id = 0
    song_id += 1
    song_path = 'music/song' + str(song_id) + '.wav'
    song = Song(user_id=user.user_id, song_path=song_path, name=name)
    db.session.add(song)
    db.session.commit()

    return jsonify({})


@app.route('/profile')
def profile():

    return render_template('profile.html')


@app.route('/logout')
def logout():

    session.pop('user')
    return redirect('/')


@app.route('/process_song', methods=['POST'])
def song():

    melody = request.form.get('melody')
    sample_song(melody)
    return jsonify({})


if __name__ == '__main__':

    connect_to_db(app)
    app.debug = True
    app.jinja_env.auto_reload = True
    app.run(port=5000, host='0.0.0.0')
