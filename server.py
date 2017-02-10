from flask import Flask, render_template, redirect, request, jsonify, session, flash
import os
from parse_music import sample_song, perm_save_song
from model import User, Song, db, connect_to_db

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def index():
    """Send respnse containing Home page"""
    return render_template('index.html')


@app.route('/profile')
def profile():

    if 'user' not in session:
        return redirect('/')

    user = User.query.filter_by(username=session['user']).first()
    user_id = user.user_id
    songs = Song.query.filter_by(user_id=user_id).all()
    return render_template('profile.html', songs=songs)


@app.route('/logout')
def logout():

    session.pop('user')
    return redirect('/')


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

    song = Song(user_id=user.user_id, name=name)

    db.session.add(song)
    db.session.flush()

    song.song_path = 'static/music/song' + str(song.song_id) + '.wav'
    perm_save_song(song.song_path)

    db.session.commit()

    return jsonify({})


@app.route('/delete_song', methods=['POST'])
def delete_song():

    song_id = int(request.form.get('song_id')[4:])
    Song.query.filter_by(song_id=song_id).delete()
    db.session.commit()

    return redirect('/profile')


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
