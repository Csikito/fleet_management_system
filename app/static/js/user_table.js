$(document).ready(function() {
    $('#userTable').DataTable({
        dom: 'lrtip',
         ajax: {
            url: '/server_side_user',
        },
        columns: [
            { title: 'Photo', data: 'image', render : function (data, type, row){
                if(data){
                   console.log(data)
                   let img = `<img src="data:image/jpeg;base64,${data}" class="img-circle elevation-2" style="width:25px; height:25px" alt="User Image">`
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
