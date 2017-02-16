var draw_other_piece = function(notes, chords) {
    var vf = new Vex.Flow.Factory({
      renderer: {selector: 'boo', width: 500, height: 230}
    });

    var score = vf.EasyScore();

    var width = 250;
    var x = 5;

    for (var i = 0; i < notes.length; i += 4) {

        var note_list = [];
        var chord_list = [];

        var system = vf.System({ x: x, y: 5, width: width, spaceBetweenStaves: 10 });
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
        console.log(note_str);
        console.log(chord_str);

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



var draw_piece = function (notes, chords) {

    var convert_note = function(note){

        if (note.length == 2) {
            var key = note[0].toLowerCase() + '/' + note[1];
        } else {
            var key = note[0].toLowerCase() + '/' + note[2];
            var accid = note[1];
        }
        return key;

    }





    // stuff that just has to be done
    var VF = Vex.Flow;
    var canvas = $('canvas')[0];
    var renderer = new VF.Renderer(canvas, VF.Renderer.Backends.CANVAS);
    var ctx = renderer.getContext();
    var formatter = new VF.Formatter();

    var new_notes = [];
    for (var i = 0; i < notes.length; i++){
        new_notes.push(convert_note(notes[i]));
    }

    var new_chords = [];
    for (var i = 0; i < chords.length; i++) {
        var c = chords[i];

        var new_c = []
        for (var j = 0; j < c.length; j++) {
            new_c.push(convert_note(c[j]));
        }
        new_chords.push(new_c);
    }

    var occurences = new_notes.map(function (e, i) {
        return [[e], new_chords[i]];
    });


    var x = occurences.length + occurences.length % 4;

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
            x_pos += size
        }

        var voice1 = new VF.Voice({num_beats: 4, beat_value: 4, resolution: Vex.Flow.RESOLUTION}).setMode(3);
        var voice2 = new VF.Voice({num_beats: 4, beat_value: 4, resolution: Vex.Flow.RESOLUTION}).setMode(3);

        var stave1_notes = [];
        var stave2_notes = [];
        for (var j = i; j < i+4; j++) {


            if (j >= occurences.length) {
                var note = new VF.GhostNote({clef: 'treble', keys: ['c/4'], duration: 'q'})
                var chord = new VF.GhostNote({clef: 'bass', keys: ['c/4'], duration: 'q'})
            } else {
                var note = new VF.StaveNote({clef: 'treble', keys: occurences[j][0], duration: 'q'})
                var chord = new VF.StaveNote({clef: 'bass', keys: occurences[j][1], duration: 'q'})
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


}





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
    $('#boo').replaceChild('<canvas width="500" height="230"></canvas>');

    $('.b').attr('disabled', true);
    var melody = $('#melody').val();
    $.post('/process_song', {'melody': melody}, function(results){

        var source = song_path + '?random=' + new Date().getTime();
        $('#audio').attr('src', source);

        // var img_source = 'static/scores/song.svg?random=' + new Date().getTime();
        // $('img').attr('src', img_source);
        draw_piece(results.notes, results.chords);
        draw_other_piece(results.notes, results.chords);

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