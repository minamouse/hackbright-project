import unittest
from music21 import corpus, stream
from parse_music import to_scale_degrees, parse_melody


class TestParseMusic(unittest.TestCase):

    def test_scale_degrees(self):

        piece = corpus.parse('bach/bwv262.mxl')
        transposed_piece = to_scale_degrees(piece)
        self.assertEqual(transposed_piece.analyze('key').name, 'C major')

    def test_parse_melody(self):

        melody = parse_melody('E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4')
        self.assertEqual(type(melody), stream.Part)


if __name__ == '__main__':
    unittest.main()
