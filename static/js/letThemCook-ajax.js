$(document).ready(function() {

    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();

        $.get('suggest/',
            {'suggestion': query},
            function(data) {
                $('#recipes-listing').html(data);
            })
        });
            
});