$(function() {
    console.log('wee')


    //event handler
    $('#btn-click').click(function() {
        if ($("input").val() !== '') {
            var input = $("input").val()
            console.log(input)

            $('ol').append('<li><a href="">x</a> - ' + input + '</li>');
        }
        $('input').val('');
    });
});

// the 'a' here refers to the anchor in the list object
$(document).on('click', 'a', function(event) {
    //removes the default action of following a link
    event.preventDefault();
    $(this).parent().remove();
});

