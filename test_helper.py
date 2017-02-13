from helper import save_file, new_song
import unittest
import os


class TestHelpers(unittest.TestCase):

    def test_new_song(self):
        # for some reason this test only passes if the other test is commented out

        os.remove('static/song.mid')
        os.remove('static/song.wav')

        truth = new_song("C5")

        assert os.path.exists('static/song.mid')
        assert os.path.exists('static/song.wav')

    def test_save_file(self):

        open('static/song.wav', 'a').close()

        path = 'static/test/'
        songname = 'song.wav'

        save_file(path, songname)
        assert os.path.exists('static/test/song.wav')

        os.remove('static/test/song.wav')
        os.rmdir('static/test')

if __name__ == '__main__':
    unittest.main()
