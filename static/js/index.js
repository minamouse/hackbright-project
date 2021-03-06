'use strict';

var draw_piece = function (notes, chords) {

    var convert_note = function(note){

        var key;
        var accid;
        var dur = note[1];

        if (note[0].length == 2) {
            var key = note[0][0].toLowerCase() + '/' + note[0][1];
            var accid = '0';
        } else {
            if (note[0] === 'r') {
                key = 'b/4';
                accid = '0';
                dur = dur + 'r';
            } else {
                var key = note[0][0].toLowerCase() + '/' + note[0][2];
                var accid = note[0][1];
                if (accid == '-') {
                    accid = 'b';
                }
            }
        }
        return [key, accid, dur];
    };


    var convert_chord = function(chord){

        var keys = [];
        var accids = [];
        var dur = chord[1];

        for (var i = 0; i < chord[0].length; i++){
            var results = convert_note([chord[0][i], 'q']);
            keys.push(results[0]);
            accids.push(results[1]);
        }

        return [keys, accids, dur];
    };

    // stuff that just has to be done
    var VF = Vex.Flow;
    var canvas = $('#score')[0];
    var renderer = new VF.Renderer(canvas, VF.Renderer.Backends.CANVAS);
    var ctx = renderer.getContext();
    var formatter = new VF.Formatter();

    var x_pos = 10;
    var size = 250;

    var stave1;
    var stave2;

    for (var m = 0; m < notes.length; m++){
        var new_notes = [];
        var new_chords = [];

        if (m == 0) {
            var stave1 = new VF.Stave(x_pos, 20, size + 50).addClef('treble').addTimeSignature('4/4');
            var stave2 = new VF.Stave(x_pos, 110, size + 50).addClef('bass').addTimeSignature('4/4');
            x_pos += size + 50;
        } else {
            var stave1 = new VF.Stave(x_pos, 20, size);
            var stave2 = new VF.Stave(x_pos, 110, size);
            x_pos += size;
        }

        for (var i = 0; i < notes[m].length; i++){
            var results = convert_note(notes[m][i]);
            new_notes.push(results);
        }

        for (var i = 0; i < chords[m].length; i++){
            var results = convert_chord(chords[m][i]);
            new_chords.push(results);
        }
        
        var voice1 = new VF.Voice({num_beats: 4, beat_value: 4, resolution: Vex.Flow.RESOLUTION}).setMode(3);
        var voice2 = new VF.Voice({num_beats: 4, beat_value: 4, resolution: Vex.Flow.RESOLUTION}).setMode(3);
        var stave1_notes = [];
        var stave2_notes = [];
        for (var j = 0; j < new_notes.length; j++) {
            
            // if (j >= occurences.length) {
            //     var note = new VF.GhostNote({clef: 'treble', keys: ['c/4'], duration: 'q'});
            //     var chord = new VF.GhostNote({clef: 'bass', keys: ['c/4'], duration: 'q'});
            // } else {

            var note = new VF.StaveNote({clef: 'treble', keys: [new_notes[j][0]], duration: new_notes[j][2], auto_stem: true});
            if (new_notes[j][1] !== '0') {
                note.addAccidental(0, new VF.Accidental(new_notes[j][1]));
            }
            if (new_notes[j][2][1] === 'd') {
                note.addDotToAll();
            }
            stave1_notes.push(note);
        }

        for (var j = 0; j < new_chords.length; j++){

            var chord = new VF.StaveNote({clef: 'bass', keys: new_chords[j][0], duration: new_chords[j][2], auto_stem: true});
            for (var l = 0; l < new_chords[j][1].length; l++) {

                if (new_chords[j][1][l] !== '0') {
                    chord.addAccidental(l, new VF.Accidental(new_chords[j][1][l]));
                }
                if (new_chords[j][2][1] == 'd') {
                    chord.addDotToAll();
                }
            }
            stave2_notes.push(chord);
        }

            
        // }

    voice1.addTickables(stave1_notes);
    voice2.addTickables(stave2_notes);
    
    formatter.format([voice1, voice2], size);

    stave1.setContext(ctx).draw();
    voice1.draw(ctx, stave1);

    stave2.setContext(ctx).draw();
    voice2.draw(ctx, stave2);
    }

};

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

var song_path = $('#download').attr('href');
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
    // $("#loading-gif").attr('hidden', false);

    $('.b').attr('disabled', true);
    var melody = $('#melody').val();
    $.post('/process_song', {'melody': melody}, function(results){
        var source = song_path + '?random=' + new Date().getTime();
        $('#audio').attr('src', source);

        $('canvas').attr('width', (results.notes.length * 250) + 50);
        draw_piece(results.notes, results.chords);

        // save canvas to image file
        var img = $('canvas')[0].toDataURL("image/png");
        $('canvas').attr('src', img);

        $('.b').attr('disabled', false);
        $('#saved').attr('style', "display: none;");
        $('#save').attr('style', '');

        if (!$('#loggedin').length) {
            $('#save').attr('disabled', true);
        }

        $('#music-result').attr('hidden', false);
        $("#loading-gif").attr('hidden', true);
        $('html, body').animate({scrollTop: $('#music-result').offset().top}, 'slow');
        $('#melody').val('');
    });
});

$('#name_submit').on('click', function(evt){
    evt.preventDefault();
    var data = {'name': $('#name_input').val(),
                'image': $('canvas').attr('src')};
    $.post('/save', data, function() {
        $('#save').attr('style', "display: none;");
        $('#saved').attr('style', '');
        $('#name_input').val('');
    });
});

var add_note = function(source, length) {
    var note = source.split('/')[2].split('.')[0];
    note = note.replace('s', '#');
    note += '\\' + length;
    var text = $('#melody').val();
    if (text === '') {
        $('#melody').val(note);
    } else {
        $('#melody').val(text + ' ' + note);
    }
};

$('#white-keys div').on('mousedown', function(event) {
    var key = $(event.target);
    key.css('border-width', '2px');
    var audio = key.children();

    add_note(audio.attr('src'), $('.selected_rhythm').attr('value'));

    audio[0].currentTime = 0;
    audio[0].play();
});

$('#white-keys div').on('mouseup', function(event) {
    $(event.target).css('border-width', '1px');
});

$('#black-keys div').on('mousedown', function(event) {
    var key = $(event.target);
    key.css('border', 'solid 1px grey');
    var audio = key.children();

    add_note(audio.attr('src'), $('.selected_rhythm').attr('value'));

    audio[0].currentTime = 0;
    audio[0].play();
});

$('#black-keys div').on('mouseup', function(event) {
    $(event.target).css('border', '');
});

$('#clear_text').on('click', function() {
    $('#melody').val('');
});


var rhythm_buttons = $('.rhythms');

rhythm_buttons.on('click', function(event) {
    rhythm_buttons.removeClass('selected_rhythm');
    $(event.target).addClass('selected_rhythm');
});

$(document).keypress(function(e) {
    console.log(e.keyCode);
    if (e.keyCode === 49){
        rhythm_buttons.removeClass('selected_rhythm');
        $('#whole').addClass('selected_rhythm');
    } else if (e.keyCode === 50){
        rhythm_buttons.removeClass('selected_rhythm');
        $('#dotted_half').addClass('selected_rhythm');
    } else if (e.keyCode === 51){
        rhythm_buttons.removeClass('selected_rhythm');
        $('#half').addClass('selected_rhythm');
    } else if (e.keyCode === 52){
        rhythm_buttons.removeClass('selected_rhythm');
        $('#dotted_quarter').addClass('selected_rhythm');
    } else if (e.keyCode === 53){
        rhythm_buttons.removeClass('selected_rhythm');
        $('#quarter').addClass('selected_rhythm');
    } else if (e.keyCode === 54){
        rhythm_buttons.removeClass('selected_rhythm');
        $('#eighth').addClass('selected_rhythm');
    } else if (e.keyCode === 55){
        rhythm_buttons.removeClass('selected_rhythm');
        $('#sixteenth').addClass('selected_rhythm');
    }
});


$('#restart-button').on('click', function(){
    $('html, body').animate({scrollTop: $('#music-input').offset().top}, 'slow');
    setTimeout(function() {$('#music-result').attr("hidden", true);}, 500);
});

$('#start-button').on('click', function(){
    $('#music-input').attr('hidden', false);
    $('html, body').animate({scrollTop: $('#music-input').offset().top}, 'slow');
    setTimeout(function() {$('#landing').attr("hidden", true);}, 500);
    $('nav').fadeIn(500);
});

