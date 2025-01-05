$(document).ready(function() {
    $('#permissionsTable').DataTable({
        dom: '<"top d-flex justify-content-between"<"d-flex align-items-center"l><"ml-auto"B>>t<"bottom"p>',
        buttons: [
            {
                text: 'New',
                className: 'btn btn-primary',
                action: function () {
                    window.location.href = '/permission_edit/0';
                }
            }
        ],
         ajax: {
            url: '/server_side_permission', // REST API végpont
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
