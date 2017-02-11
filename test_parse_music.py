import unittest
from music21 import stream, note


class TestParseMusic(unittest.TestCase):

    def setUp(self):

        # create song with four parts in F major
        self.song_orig = stream.Stream()
        orig_part_lists = [['F5', 'D5',  'E5',  'F5'],
                           ['C5', 'B-4', 'B-4', 'C5'],
                           ['A4', 'F4',  'G4',  'A4'],
                           ['F3', 'B-2', 'C3',  'F3']]

        for part in orig_part_lists:
            part_stream = stream.Part()

            for note_str in part:
                part_stream.append(note.Note(note_str))

            self.song_orig.append(part_stream)

        # create the same song but in C major
        self.song_c = stream.Stream()
        c_part_lists = [['C5', 'A4', 'B4', 'C5'],
                        ['G4', 'F4', 'F4', 'G4'],
                        ['E4', 'C4', 'D4', 'E4'],
                        ['C3', 'F2', 'G2', 'C3']]

        for part in c_part_lists:
            part_stream = stream.Part()

            for note_str in part:
                measure = stream.Measure()
                measure.append(note.Note(note_str))
                part_stream.append(measure)

            self.song_c.append(part_stream)
