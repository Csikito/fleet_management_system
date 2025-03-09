$(document).ready(function() {
    $('#vehicleTable').DataTable({
        serverSide: true,
        processing: true,
        order:[[1, "asc"]],
        dom: '<"top d-flex justify-content-between"<"d-flex align-items-center"l><"ml-auto"B>>t<"bottom"p>',
        buttons: [
            {
                text: 'New',
                action: function () {
                    window.location.href = '/vehicle_edit/0';
                }
            }
        ],
         ajax: {
            url: '/server_side_vehicle',
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
            { title: 'Vehicle image', data: 'image', render : function (data, type, row){
                if(data){
                   let img = `<img src="data:;base64,${data}" class="img-circle elevation-2" style="width:35px; height:35px" alt="User Image">`
                   return img
                }
                else{
                    return `<i class="fas fa-car-tunnel fa-xl ml-1"></i>`
                }
            }},
            { title: 'Type', data: 'type' , render : function (data, type, row){
                return `<a href="/vehicle_edit/${row.id}">${data}</a>`
            }},
            { title: 'Manufacturer/Model', data: 'model' },
            { title: 'Licence Plate', data: 'plate' },
            { title: 'Driver', data: 'driver' }
        ]
    });
  });
