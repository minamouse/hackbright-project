from flask import Flask, render_template, redirect, request, session, jsonify
from helper import new_song, save_file, save_image, validate_input
from model import User, Song, db, connect_to_db
import shutil
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

if not os.path.exists('static/user_files'):
    os.makedirs('static/user_files')


@app.route('/')
def index():
    """Loads homepage."""

    if 'user_id' in session:
        user = User.query.filter_by(user_id=session['user_id']).first()
        song_path = 'static/user_files/user' + str(user.user_id) + '/temp/temp_song.wav'
        return render_template('index.html', song_path=song_path, username=user.username)

    return render_template('index.html', song_path='static/user_files/user/temp/temp_song.wav')


@app.route('/profile')
def profile():
    """If logged in, loads user's profile page."""

    if 'user_id' not in session:
        return redirect('/')

    user = User.query.filter_by(user_id=session['user_id']).first()
    songs = Song.query.filter_by(user_id=session['user_id']).all()

    return render_template('profile.html', songs=songs, username=user.username)


@app.route('/logout')
def logout():
    """If logged in, logs user out and redirects to homepage."""

    if 'user_id' in session:
        song_path = 'static/user_files/user' + str(session['user_id']) + '/temp/temp_song.wav'
        if os.path.exists(song_path):
            os.remove(song_path)

        session.pop('user_id')

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
            session['user_id'] = user.user_id
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

    session['user_id'] = user.user_id
    db.session.commit()

    results['success'] = True

    return jsonify(results)


@app.route('/save', methods=['POST'])
def save_song():
    """Handles saving songs to database.

    Saves song file to a new filename and logs it into the database.
    """

    if 'user_id' not in session:
        return ''

    name = request.form.get('name')
    image_data = request.form.get('image')
    print image_data

    song = Song(user_id=session['user_id'], name=name)

    db.session.add(song)
    db.session.flush()

    path = 'static/user_files/user%i/' % (session['user_id'])

    music_path = path + 'music/'
    image_path = path + 'scores/'

    music_file = 'song' + str(song.song_id) + '.wav'
    image_file = 'song_score' + str(song.song_id) + '.png'

    save_file(music_path, music_file, session['user_id'])
    save_image(image_path, image_file, image_data)

    song.song_path = music_path + music_file
    song.score_path = image_path + image_file
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

    user_path = 'static/user_files/user' + str(session['user_id'])
    shutil.rmtree(user_path)

    Song.query.filter_by(user_id=session['user_id']).delete()
    User.query.filter_by(user_id=session['user_id']).delete()

    db.session.commit()
    session.pop('user_id')

    return '/'


@app.route('/process_song', methods=['POST'])
def song():
    """Processes creating a new song."""

    melody = request.form.get('melody')

    if not validate_input(melody):
        return jsonify({'success': False})

    if 'user_id' in session:
        notes, chords = new_song(melody, session['user_id'])
    else:
        notes, chords = new_song(melody)

    data = {'notes': notes, 'chords': chords, 'success': True}

    return jsonify(data)


if __name__ == '__main__':

    connect_to_db(app)
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    app.run(port=5000, host='0.0.0.0')
