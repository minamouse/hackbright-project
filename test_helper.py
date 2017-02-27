from helper import save_file, new_song, save_image, combine_notes_and_chords, parse_melody
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

    def test_parse_melody(self):

        result = parse_melody('C4 rest')

        self.assertEqual(type(result[0]), stream.Part)
        self.assertEqual(result[1], [0, 12])
        self.assertEqual(result[2], ['C4', 'r'])

if __name__ == '__main__':
    unittest.main()
