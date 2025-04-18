$(document).ready(function() {
    $('#permissionsTable').DataTable({
        serverSide: true,
        processing: true,
        order:[[0, "asc"]],
        dom: '<"top d-flex justify-content-between"<"d-flex align-items-center"l><"ml-auto"B>>t<"bottom"p>',
        buttons: [
            {
                text: 'New',
                action: function () {
                    window.location.href = '/permission_edit/0';
                }
            }
        ],
         ajax: {
            url: '/server_side_permission',
            type: 'GET',
             data: function(d) {
                let order_column = 1;
                let order_dir = 'asc';

                if (d.order && d.order.length > 0) {
                    order_column = d.order[0].column;
                    order_dir = d.order[0].dir;
                }

                return {
                    start: d.start || 0,
                    length: d.length || 10,
                    draw: d.draw || 1,
                    order_column: order_column,
                    order_dir: order_dir
                };
            }
        },
        columns: [
            { title: 'ID', data: 'id' },
            { title: 'Name', data: 'name' , render : function (data, type, row){
                return `<a href="/permission_edit/${row.id}">${data}</a>`
            }},
            { title: 'Permissions', data: 'permissions' }
        ]
    });
  });
