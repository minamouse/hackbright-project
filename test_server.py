import unittest
from server import app
from model import db, connect_to_db, test_data


class TestServerUser(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_logout(self):

        result = self.client.get('/logout', follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('login', result.data)

    def test_process_song(self):

        data = {'melody': 'C4'}

        result = self.client.post('/process_song', data=data)

        self.assertEqual(result.status_code, 200)


class TestServerNoUser(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_key'
        self.client = app.test_client()

    def test_index_no_user(self):

        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('Name it before you save it', result.data)
        self.assertIn('login', result.data)

    def test_profile_no_user(self):

        result = self.client.get('/profile', follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertNotIn('Your saved songs', result.data)
        self.assertIn('Name it before you save it', result.data)

    def test_save_no_user(self):

        result = self.client.get('/save')
        self.assertEqual(result.status_code, 405)


class TestServerWithDB(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_key'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

    def tearDown(self):

        db.session.close()
        db.drop_all()

    def test_signin(self):

        data = {'username': 'my name', 'password': 'my pword'}

        result = self.client.post('/signin.json', data=data, follow_redirects=True)
        self.assertIn('Username or password incorrect', result.data)

    def test_signup(self):

        data = {'username': 'user', 'password': '1234'}

        result = self.client.post('/signup.json', data=data)

        self.assertEqual(result.status_code, 200)


class TestServerWithUserAndDB(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        test_data()

    def tearDown(self):

        db.session.close()
        db.drop_all()

    def test_index_user(self):

        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('Name it before you save it', result.data)
        self.assertIn('logout', result.data)

    def test_profile_user(self):

        result = self.client.get('/profile', follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('Your saved songs', result.data)

    def test_process_song(self):

        data = {'melody': 'C4'}
        result = self.client.post('/process_song', data=data)

        self.assertEqual(result.status_code, 200)

    def test_save_song(self):

        sample_image_string = 'data:image/png;base64,iVBORw='
        data = {'name': 'song', 'image': sample_image_string}

        result = self.client.post('/save', data=data, follow_redirects=True)

        self.assertEqual(result.status_code, 200)

    def test_delete_song(self):

        data = {'song_id': 'song1'}

        result = self.client.post('/delete_song', data=data, follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertNotIn('static/music/song1.wav', result.data)

    def test_signin(self):

        data = {'username': 'username', 'password': 'password'}

        result = self.client.post('/signin.json', data=data)

        self.assertEqual(result.status_code, 200)

    def test_signup(self):

        data = {'username': 'username', 'password': 'password'}

        result = self.client.post('/signup.json', data=data)

        self.assertIn('message', result.data)

    def test_delete_profile(self):

        result = self.client.get('/delete_profile')
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
