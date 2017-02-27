from helper import save_file, new_song, save_image, combine_notes_and_chords
from music21 import stream, note
import unittest
import shutil
import os


class TestHelpers(unittest.TestCase):

    def setUp(self):

        # create files
        os.makedirs('static/user_files/usertest/temp')
        open('static/user_files/usertest/temp/temp_song.wav', 'a').close()

    def tearDown(self):

        # delete files
        shutil.rmtree('static/user_files/usertest')

    def test_new_song(self):

        melody = 'C4'
        results = new_song(melody, 'test')

        self.assertEqual(results[0], [melody])
        self.assertTrue(os.path.exists('static/user_files/usertest/temp/temp_song.wav'))
        self.assertTrue(os.path.exists('static/user_files/usertest/temp/temp_song.mid'))

    def test_save_file(self):

        path = 'static/user_files/usertest/music/'
        filename = 'song.wav'
        user_id = 'test'
        save_file(path, filename, user_id)

        self.assertTrue(os.path.exists(path + filename))

    def test_save_image(self):

        image = 'data:image/png;base64,iVBORw='
        path = 'static/user_files/usertest/scores/'
        filename = 'song_score1.png'

        save_image(path, filename, image)

        self.assertTrue(os.path.exists(path + filename))

    def test_combine_notes_chords(self):

        melody = stream.Stream()

        n = note.Note('C4')
        n2 = note.Note('C4')
        melody.append(n)
        melody.append(n2)

        result = combine_notes_and_chords(melody, [['C3', 'rest']])
        self.assertEqual(type(result), stream.Stream)

if __name__ == '__main__':
    unittest.main()
