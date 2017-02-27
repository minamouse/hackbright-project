from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User table in database. Holds user_id, username and password."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)


class Song(db.Model):
    """Song table in database.

    Holds song_id, user_id of the user who created
    the song, given song name, if it exists, and song_path.
    """

    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(40), nullable=True)
    song_path = db.Column(db.String(50), nullable=True)
    score_path = db.Column(db.String(50), nullable=True)


def connect_to_db(app, db_name='postgresql:///project'):
    """Connect to the database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


def test_data():
    """Create some sample data for testing.
    """

    user = User(username='username', password='password')
    song = Song(user_id=1, name='song', song_path='static/user_files/user1/music/song1.wav')

    db.session.add(user)
    db.session.commit()
    db.session.add(song)
    db.session.commit()


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
