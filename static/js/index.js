"use strict";

var x = document.getElementById('audio');

$('#play').on('click', function() {
    x.play();
});

$('#pause').on('click', function() { 
    x.pause();
});

$('#stop').on('click', function() { 
    x.pause();
    x.currentTime = 0;
});

$('#save').on('click', function() {
    $('#save').attr('style', "display: none;");
    $('#saved').attr('style', '');
});

$('#mel_submit').on('click', function(evt){
    evt.preventDefault();
    $('.b').attr('disabled', true);
    var melody = $('#melody').val();
    $.post('/process_song', {'melody': melody}, function(){

        var source = 'static/song.wav?random=' + new Date().getTime();
        $('#audio').attr('src', source);
        $('.b').attr('disabled', false);
        $('#saved').attr('style', "display: none;");
        $('#save').attr('style', '');
    });
});


$('#name_submit').on('click', function(evt){
    evt.preventDefault();
    var song_name = $('#name_input').val();
    var data = {'name': song_name};
    $.post('/save', data);
});
