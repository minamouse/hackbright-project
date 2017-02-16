from music21 import note, stream, midi
import subprocess
import os


all_notes = []

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
octaves = ['3', '4', '5']
accidentals = ['', '#']

for l in letters:
    for o in octaves:
        for a in accidentals:

            all_notes.append(l+o+a)

for this_note in all_notes:

    my_note = note.Note(this_note)
    new_song = stream.Stream()
    new_song.append(my_note)

    mid = 'sound/' + this_note + '.mid'
    wav = 'static/sounds/' + this_note + '.wav'

    mf = midi.translate.streamToMidiFile(new_song)
    mf.open(mid, 'wb')
    mf.write()
    mf.close()

    # convert to .wav format
    subprocess.call(['timidity ' + mid + ' -Ow -o ' + wav], shell=True)
