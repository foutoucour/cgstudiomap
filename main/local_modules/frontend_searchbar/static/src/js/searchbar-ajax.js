// Routing of autocompletion for the search bar
$("#autocomplete").autocomplete({
    minLength: 2,
    source: function (request, response) {
        // return a list of mapping such as
        // [{"label": "value (type)", "data": "value"}]
        $.ajax({
            url: "/ajax/search_bar/get_auto_complete_search_values",
            data: {term: request.term},
            success: function (data) {response($.parseJSON(data));}
        });
    },
    // preventDefault prevents the field to be filled with label and it is now filled by data.
    select: function(event, ui) {
        event.preventDefault();
        $("#autocomplete").val(ui.item.data);
    },
    focus: function(event, ui) {
        event.preventDefault();
        $("#autocomplete").val(ui.item.data);
    }
});

