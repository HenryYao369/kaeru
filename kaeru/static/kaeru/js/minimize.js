$(function() {
    $('button').click(function() {
        // Resize directory
        var directory = $('#directory');
        directory.toggleClass('small-1');
        directory.toggleClass('small-2');

        // Resize content
        var code = $('#code');
        code.toggleClass('small-4');
        code.toggleClass('small-3');

    });
});