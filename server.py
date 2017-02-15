from flask import Flask, render_template, redirect, request, session, jsonify
from model import User, Song, db, connect_to_db
from helper import new_song, save_file
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def index():
    """Loads homepage."""

    if 'user' in session:
        user = User.query.filter_by(user_id=session['user']).first()
        song_path = 'static/song' + str(user.user_id) + '.wav'
        return render_template('index.html', song_path=song_path, username=user.username)

    return render_template('index.html', song_path='static/song.wav')


@app.route('/profile')
def profile():
    """If logged in, loads user's profile page."""

    if 'user' not in session:
        return redirect('/')

    user = User.query.filter_by(user_id=session['user']).first()
    songs = Song.query.filter_by(user_id=session['user']).all()

    return render_template('profile.html', songs=songs, username=user.username)


@app.route('/logout')
def logout():
    """If logged in, logs user out and redirects to homepage."""

    if 'user' in session:
        for music_file in os.listdir('static'):
            if music_file[4:-4] == str(session['user']):
                os.remove('static/' + music_file)

        session.pop('user')

    return redirect('/')


@app.route('/signin.json', methods=['POST'])
def signin():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    results = {}

    if user:
        if user.password == password:
            results['success'] = True
            session['user'] = user.user_id
            return jsonify(results)

    results['success'] = False
    message = 'Username or password incorrect.'
    results['message'] = message

    return jsonify(results)


@app.route('/signup.json', methods=['POST'])
def signup():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    results = {}
    if user:
        results['success'] = False
        message = 'Username is taken!'
        results['message'] = message
        return jsonify(results)

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.flush()

    session['user'] = user.user_id
    db.session.commit()

    results['success'] = True

    return jsonify(results)


@app.route('/save', methods=['POST'])
def save_song():
    """Handles saving songs to database.

    Saves song file to a new filename and logs it into the database.
    """

    name = request.form.get('name')

    song = Song(user_id=session['user'], name=name)

    db.session.add(song)
    db.session.flush()

    path = 'static/music/'
    filename = 'song' + str(song.song_id) + '.wav'

    if 'user' in session:
        save_file(path, filename, session['user'])
    else:
        save_file(path, filename)

    song.song_path = path + filename
    db.session.commit()
    return ''


@app.route('/delete_song', methods=['POST'])
def delete_song():
    """Deletes song from database."""

    song_id = int(request.form.get('song_id')[4:])
    Song.query.filter_by(song_id=song_id).delete()
    db.session.commit()

    return '/profile'


@app.route('/delete_profile')
def delete_profile():
    """Deletes users profile."""

    songs = Song.query.filter_by(user_id=session['user']).all()
    for song in songs:
        path = song.song_path
        os.remove(path)

    Song.query.filter_by(user_id=session['user']).delete()
    User.query.filter_by(user_id=session['user']).delete()

    db.session.commit()
    session.pop('user')

    return '/'


@app.route('/process_song', methods=['POST'])
def song():
    """Processes creating a new song."""

    melody = request.form.get('melody')

    if 'user' in session:
        notes, chords = new_song(melody, session['user'])
    else:
        notes, chords = new_song(melody)

    data = {'notes': notes, 'chords': chords}

    return jsonify(data)


if __name__ == '__main__':

    connect_to_db(app)
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    app.run(port=5000, host='0.0.0.0')
