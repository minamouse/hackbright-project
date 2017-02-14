"use strict";

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
    $.post('/process_song', {'melody': melody}, function(){

        var source = song_path + '?random=' + new Date().getTime();
        $('#audio').attr('src', source);
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
