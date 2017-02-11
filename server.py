from flask import Flask, render_template, redirect, request, session, flash
from model import User, Song, db, connect_to_db
from parse_music import new_song
import subprocess
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def index():
    """Loads homepage."""

    return render_template('index.html')


@app.route('/profile')
def profile():
    """If logged in, loads user's profile page."""

    if 'user' not in session:
        return redirect('/')

    user = User.query.filter_by(username=session['user']).first()
    user_id = user.user_id
    songs = Song.query.filter_by(user_id=user_id).all()

    return render_template('profile.html', songs=songs)


@app.route('/logout')
def logout():
    """If logged in, logs user out and redirects to homepage."""

    if 'user' in session:
        session.pop('user')

    return redirect('/')


@app.route('/login', methods=['POST'])
def process_login():
    """Handles user login.

    If username exists in database, checks the given password and logs them in,
    or flashes an error message. If the username does not exist, creates new
    user account automatically.
    """

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
    """Handles saving songs to database.

    If user is not logged in, flashes error message. Otherwise, saves song file
    to a new filename and logs it into the database.
    """

    if 'user' not in session:
        flash('Please log in to save your songs!')
        return redirect('/')

    name = request.form.get('name')
    user = User.query.filter_by(username=session['user']).first()

    song = Song(user_id=user.user_id, name=name)

    db.session.add(song)
    db.session.flush()

    subprocess.call(['mkdir static/music'], shell=True)
    song.song_path = 'static/music/song' + str(song.song_id) + '.wav'

    command = 'mv static/song.wav ' + song.song_path
    subprocess.call([command], shell=True)

    db.session.commit()

    return 'Successful'


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

    user = User.query.filter_by(username=session['user']).first()

    Song.query.filter_by(user_id=user.user_id).delete()
    User.query.filter_by(user_id=user.user_id).delete()

    db.session.commit()
    session.pop('user')

    return '/'


@app.route('/process_song', methods=['POST'])
def song():
    """Processes creating a new song."""

    melody = request.form.get('melody')
    new_song(melody)

    return ''


if __name__ == '__main__':

    connect_to_db(app)
    app.debug = True
    app.jinja_env.auto_reload = True
    app.run(port=5000, host='0.0.0.0')
