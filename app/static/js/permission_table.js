$(document).ready(function() {
    console.log("asd")
    $('#permissionsTable').DataTable({
        dom: 'lrtip',
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
