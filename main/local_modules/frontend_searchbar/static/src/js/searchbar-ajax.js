// Routing of autocompletion for the search bar
var options = {
    url: "/ajax/search_bar/get_auto_complete_search_values",

    ajaxSettings: {
        dataType: "json",
        method: "post",
        data: {}
    },
    list: {
        match: {
            enabled: true
        },
        maxNumberOfElements: 8
    },
    preparePostData: function (data) {
        data.term = $("#autocomplete").val();
        return data;
    },
    theme: "square"

};

$("#autocomplete").easyAutocomplete(options);
