"use strict";

var delete_song;

$('.play').on('click', function(event) {
    var song_id = event.target.parentNode.id;
    var audio_id = song_id.replace('song', 'play');
    var x = document.getElementById(audio_id);

    x.play();
});

$('.pause').on('click', function(event) {
    var song_id = event.target.parentNode.id;
    var audio_id = song_id.replace('song', 'play');
    var x = document.getElementById(audio_id);
    x.pause();
});

$('.stop').on('click', function(event) {
    var song_id = event.target.parentNode.id;
    var audio_id = song_id.replace('song', 'play');
    var x = document.getElementById(audio_id);
    x.pause();
    x.currentTime = 0;
});

$('.unsave').on('click', function(event) {
    delete_song = event.target.parentNode.id;
});

$('#confirm_delete').on('click', function() {
    var data = {'song_id': delete_song};
    $.post('/delete_song', data, function(result) {
        window.location.href = result;
    });
});

$('#confirm_profile_delete').on('click', function() {
    $.get('/delete_profile', function(result) {
        window.location.href = result;
    });
});