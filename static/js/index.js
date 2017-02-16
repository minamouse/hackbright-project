
var draw_piece = function (notes, chords) {

    var convert_note = function(note){

        console.log(note);
        if (note.length == 2) {
            var key = note[0].toLowerCase() + '/' + note[1];
            var accid = '0';
        } else {
            var key = note[0].toLowerCase() + '/' + note[2];
            var accid = note[1];
            if (accid == '-') {
                accid = 'b';
            }
        }
        return [key, accid];

    };


    // stuff that just has to be done
    var VF = Vex.Flow;
    var canvas = $('canvas')[0];
    var renderer = new VF.Renderer(canvas, VF.Renderer.Backends.CANVAS);
    var ctx = renderer.getContext();
    var formatter = new VF.Formatter();

    var new_notes = [];
    var note_accids = [];
    for (var i = 0; i < notes.length; i++){
        var results = convert_note(notes[i]);
        new_notes.push(results[0]);
        note_accids.push(results[1]);
    }
    var new_chords = [];
    var chord_accids = [];
    for (var i = 0; i < chords.length; i++) {
        var c = chords[i];

        var new_c = [];
        var accids = [];
        for (var j = 0; j < c.length; j++) {
            var results = convert_note(c[j]);
            new_c.push(results[0]);
            accids.push(results[1]);
        }
        new_chords.push(new_c);
        chord_accids.push(accids);
    }

    var occurences = new_notes.map(function (e, i) {
        return [[e], new_chords[i]];
    });

    var accidentals = note_accids.map(function (e, i) {
        return [e, chord_accids[i]];
    });

    console.log(occurences.length % 4);
    var x = occurences.length + (4 - (occurences.length % 4));
    console.log(x);

    var x_pos = 10;
    var size = 200;

    for (var i = 0; i < x; i+=4) {

        if (i == 0) {
            var stave1 = new VF.Stave(x_pos, 20, size + 50).addClef('treble').addTimeSignature('4/4');
            var stave2 = new VF.Stave(x_pos, 110, size+ 50).addClef('bass').addTimeSignature('4/4');
            x_pos += size + 50
        } else {

            var stave1 = new VF.Stave(x_pos, 20, size);
            var stave2 = new VF.Stave(x_pos, 110, size);
            x_pos += size;
        }

        var voice1 = new VF.Voice({num_beats: 4, beat_value: 4, resolution: Vex.Flow.RESOLUTION}).setMode(3);
        var voice2 = new VF.Voice({num_beats: 4, beat_value: 4, resolution: Vex.Flow.RESOLUTION}).setMode(3);

        var stave1_notes = [];
        var stave2_notes = [];
        for (var j = i; j < i+4; j++) {

// addAccidental(2, new VF.Accidental("#")).
// addAccidental(3, new VF.Accidental("n"))
            
            if (j >= occurences.length) {
                console.log("i am adding a gnote");
                var note = new VF.GhostNote({clef: 'treble', keys: ['c/4'], duration: 'q'});
                console.log("i am adding a gchord");
                var chord = new VF.GhostNote({clef: 'bass', keys: ['c/4'], duration: 'q'});
            } else {
                console.log("i am adding a note");
                var note = new VF.StaveNote({clef: 'treble', keys: occurences[j][0], duration: 'q'});
                console.log("i am adding a chord");
                var chord = new VF.StaveNote({clef: 'bass', keys: occurences[j][1], duration: 'q'});

                if (accidentals[j][0] !== '0') {
                    note.addAccidental(0, new VF.Accidental(accidentals[j][0]));
                }
                for (var l = 0; l < accidentals[j][1].length; l++) {
                    if (accidentals[j][1][l] !== '0') {
                        chord.addAccidental(l, new VF.Accidental(accidentals[j][1][l]));
                    }
                }
            
            }

            stave1_notes.push(note);
            stave2_notes.push(chord);

        }


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
    // $('#boo').replaceWith('<div id="boo" class="img-rounded" style="text-align: center; background: rgba(255,255,255,0.7); margin-left: auto; margin-right: auto;"><canvas width="500" height="230"></canvas></div>');

    $('.b').attr('disabled', true);
    var melody = $('#melody').val();
    $.post('/process_song', {'melody': melody}, function(results){

        var source = song_path + '?random=' + new Date().getTime();
        $('#audio').attr('src', source);

        // var img_source = 'static/scores/song.svg?random=' + new Date().getTime();
        // $('img').attr('src', img_source);
        $('canvas').attr('width', (Math.ceil(results.notes.length/4) * 200) + 80);
        // console.log((Math.ceil(results.notes.length/4) * 200) + 50);
        draw_piece(results.notes, results.chords);
        // draw_other_piece(results.notes, results.chords);

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


// save canvas to image file
// var img = canvas.toDataURL("image/png");