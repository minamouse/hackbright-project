'use strict';

$('#signin').on('click', function(evt) {
    evt.preventDefault();
    var data = {'username': $('#inputUserName').val(),
                'password': $('#inputPassword').val()
            };

    $.post('/signin.json', data, function(result) {
        console.log(result);
        if (result.success) {
            location.reload();
        } else {
            $('#flash').html(result.message);
            $('#flash').attr('hidden', false);
            $('#inputPassword').val('');
        }
    });
})

$('#signup').on('click', function(evt) {
    evt.preventDefault();
    var data = {'username': $('#inputUserName').val(),
                'password': $('#inputPassword').val()
            };

    $.post('/signup.json', data, function(result) {
        if (result.success) {
            location.reload();
        } else {
            $('#flash').html(result.message);
            $('#flash').attr('hidden', false);
            $('#inputPassword').val('');
            $('#inputUserName').val('');
        }
    });
})