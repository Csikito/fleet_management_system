$(document).ready(function() {
    $('#vehicleTable').DataTable({
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
            { title: 'Driver', data: 'driver' }
        ]
    });
  });
