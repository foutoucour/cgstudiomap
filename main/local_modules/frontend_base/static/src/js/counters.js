/**
 *
 * Created by foutoucour on 1/1/16.
 */

//Get the count of users
//The result will be display in the target
function get_user_count_ajax(target) {
    $.ajax({
        type: "post",
        url: '/directory/get_user_count_json',
        success: function (response) {
            var data = JSON.parse(response);
            $(target).text(data['counter']);
        }
    })
}

//Get the count of company following the given criteria
function get_company_count_ajax(search, status, target) {
    console.log('search: ' + search);
    console.log('status: ' + status);
    $.ajax({
        type: "post",
        url: '/directory/get_company_count_json',
        data: {search: search, company_status: status},
        success: function (response) {
            var data = JSON.parse(response);
            console.log(data);
            $(target).text(data['counter']);
        }
    })
}
