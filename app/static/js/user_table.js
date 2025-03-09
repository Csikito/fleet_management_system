$(document).ready(function() {
    $('#userTable').DataTable({
        dom: '<"top d-flex justify-content-between"<"d-flex align-items-center"l><"ml-auto"B>>t<"bottom"p>',
        serverSide: true,
        processing: true,
        order:[[1, "asc"]],
        buttons: [
            {
                text: 'New',
                action: function () {
                    window.location.href = '/user_edit/0';
                }
            }
        ],
        ajax: {
            url: '/server_side_user',
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
            { title: 'Photo', data: 'image', render : function (data, type, row){
                if(data){
                   let img = `<img src="data:;base64,${data}" class="img-circle elevation-2" style="width:25px; height:25px" alt="User Image">`
                   return img
                }
                else{
                    return `<i class="fas fa-circle-user"></i>`
                }
            }},
            { title: 'Name', data: 'name' , render : function (data, type, row){
                return `<a href="/user_edit/${row.id}">${data}</a>`
            }},
            { title: 'Username', data: 'username' },
            { title: 'Permission', data: 'permission' }
        ]
    });
  });
