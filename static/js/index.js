"use strict";


var draw_piece = function(notes, chords) {

    var vf = new Vex.Flow.Factory({
      renderer: {selector: 'boo', width: 1000, height: 500}
    });

    var score = vf.EasyScore();

    var width = 250;
    var x = 10;

    for (var i = 0; i < notes.length; i += 4) {

        var note_list = [];
        var chord_list = [];

        var system = vf.System({ x: x, y: 80, width: width, spaceBetweenStaves: 10 });
        for (var j = i; j < i+4; j++) {

            if (j < notes.length) {
                note_list.push(notes[j] + '/q');
                chord_list.push('(' + chords[j].join(' ') + ')/q');
            } else {
                note_list.push('B4/q/r');
                chord_list.push('D3/q/r');
            }
        }
        var note_str = note_list.join(', ');
        var chord_str = chord_list.join(', ');

        if (i === 0) {
            system.addStave({
              voices: [
                score.voice(score.notes(note_str)),
              ]
            }).addClef('treble').addTimeSignature('4/4');

            system.addStave({
              voices: [
                score.voice(score.notes(chord_str, {clef: 'bass'}))
              ]
            }).addClef('bass').addTimeSignature('4/4');

            system.addConnector();

        } else {

            system.addStave({
              voices: [
                score.voice(score.notes(note_str)),
              ]
            });

            system.addStave({
              voices: [
                score.voice(score.notes(chord_str, {clef: 'bass'}))
              ]
            });

        }

        x += width;
    }

    vf.draw();
};

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

var song_path = $('#path_form').attr('action');

var audio = $("#audio")[0];

$('#play').on('click', function() {
    audio.play();
});

$('#pause').on('click', function() {
    audio.pause();
});

$('#stop').on('click', function() {
    audio.pause();
    audio.currentTime = 0;
});


$('#mel_submit').on('click', function(evt){
    evt.preventDefault();
    $('.b').attr('disabled', true);
    var melody = $('#melody').val();
    $.post('/process_song', {'melody': melody}, function(results){

        var source = song_path + '?random=' + new Date().getTime();
        $('#audio').attr('src', source);

        draw_piece(results.notes, results.chords);

        $('.b').attr('disabled', false);
        $('#saved').attr('style', "display: none;");
        $('#save').attr('style', '');

        if (!$('#loggedin').length) {
            $('#save').attr('disabled', true);
        }

    });
});


$('#name_submit').on('click', function(evt){
    evt.preventDefault();
    var song_name = $('#name_input').val();
    var data = {'name': song_name};
    $.post('/save', data, function() {
        $('#save').attr('style', "display: none;");
        $('#saved').attr('style', '');
    });
});
