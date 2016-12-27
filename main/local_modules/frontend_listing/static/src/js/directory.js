function bootstrap_table_ajax(search, status) {
    $.ajax({
        type: "post",
        url: "/directory/get_partners",
        data: {search: search, company_status: status},

        complete: function () {
            $('.loading-spinner').hide();
        },

        success: function (response) {
            var data = JSON.parse(response);
            $('table').bootstrapTable({
                classes: 'table table-no-bordered table-hover',
                height: getHeight(),
                striped: true,
                undefinedText: '&nbsp;',
                iconsPrefix: 'glyphicon',
                iconSize: 'md',
                cache: true,
                pageSize: 25,

                pagination: true,
                onlyInfoPagination: false,
                showHeader: true,
                paginationVAlign: 'bottom',

                align: 'left',
                halign: 'center',
                falign: 'right',
                valign: 'middle',
                sortable: true,
                showColumns: false,

                locale: 'en-US',
                columns: [
                    {
                        field: 'state',
                        title: ''

                    },
                    {
                        field: 'logo',
                        title: 'Logo'

                    },
                    {
                        field: 'name',
                        title: 'Name',
                        sortable: true
                    },
                    {
                        field: 'email',
                        title: 'Email'
                    },
                    {
                        field: 'industries',
                        title: 'Industries',
                        sortable: true
                    },
                    {
                        field: 'city',
                        title: 'City',
                        sortable: true
                    },
                    {
                        field: 'country_name',
                        title: 'Country',
                        sortable: true
                    }
                ],
                data: data
            });

        }
    });
}

function getHeight() {
    return $(window).height() - $('.navDirectory').outerHeight(true) - $('footer').outerHeight(true) + 8;
}


(function ($) {
    'use strict';
    $.fn.bootstrapTable.locales['en-US'] = {
        formatLoadingMessage: function () {
            return 'Loading, please wait...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' Studios per page';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return '';
        },
        formatSearch: function () {
            return 'Search';
        },
        formatNoMatches: function () {
            return 'No matching records found';
        },
        formatPaginationSwitch: function () {
            return 'Hide/Show pagination';
        },
        formatRefresh: function () {
            return 'Refresh';
        },
        formatToggle: function () {
            return 'Toggle';
        },
        formatColumns: function () {
            return 'Columns';
        },
        formatAllRows: function () {
            return 'All';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['en-US']);

})(jQuery);