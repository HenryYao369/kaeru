$(function() {
    $('button').click(function() {
        // Resize directory
        var directory = $('#directory');
        directory.toggleClass('small-3');
        directory.toggleClass('small-2');

        // Resize content
        var code = $('#code');
        code.toggleClass('small-2');
        code.toggleClass('small-3');

    });
});