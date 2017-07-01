// Routing of autocompletion for the search bar
$("#autocomplete").autocomplete({
    minLength: 2,
    source: function (request, response) {
        // return a list of mapping such as
        // [{"label": "value (type)", "data": "value"}]
        $.ajax({
            url: "/ajax/search_bar/get_auto_complete_search_values",
            data: {term: request.term},
            success: function (data) {
                response($.parseJSON(data));
            }
        });
    }
});

