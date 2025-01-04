$(document).ready(function() {
    $('#vehicleTable').DataTable({
        dom: 'lrtip',
         ajax: {
            url: '/server_side_vehicle',
        },
        columns: [
            { title: 'Vehicle image', data: 'image', render : function (data, type, row){
                if(data){
                   console.log(data)
                   let img = `<img src="data:image/jpeg;base64,${data}" class="img-circle elevation-2" style="width:50px; height:50px" alt="User Image">`
                   return img
                }
                else{
                    return `<i class="fas fa-circle-user"></i>`
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
