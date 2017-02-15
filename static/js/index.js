"use strict";



var vf = new Vex.Flow.Factory({
  renderer: {selector: 'boo', width: 1000, height: 500}
});

var score = vf.EasyScore();
var system = vf.System();





$(function () {
    $('[data-toggle="tooltip"]').tooltip()
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

        var chords = results.chords

        var new_chords = [];

        for (var i = 0; i < chords.length; i++) {
            new_chords.push('(' + chords[i].join(' ') + ')');
        }

        var notes = results.notes.join(', ')
        var chords = new_chords.join(', ')


        system.addStave({
          voices: [
            score.voice(score.notes(notes)),
          ]
        }).addClef('treble').addTimeSignature('4/4');

        system.addStave({
          voices: [
            score.voice(score.notes(chords, {clef: 'bass'}))
          ]
        }).addClef('bass').addTimeSignature('4/4');

        system.addConnector()
        vf.draw();



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
