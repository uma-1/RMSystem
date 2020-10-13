$(document).ready(function () {
    $('#myModal').on('shown.bs.modal', function () {
      $('#myInput').trigger('focus')
    });

    $('#submit1').on('click', function (e) {
        e.preventDefault();
       let name = $('#id_name').val();
       let email = $('#id_email').val();
       let phone = $('#id_phoneno').val();
       let message = $('#id_message').val();

     if (name == '')
     {
     Swal.fire({
              icon: 'error',
              title: 'Please enter your name',
              confirmButtonColor: '#9fb300',
              timer: 4000
             })
     }

    else if(email == '')
    {
    Swal.fire({
              icon: 'error',
              title: 'Please enter your email',
              confirmButtonColor: '#9fb300',
              timer: 4000
             })


     }

    else if(phone == ''){
     Swal.fire({
              icon: 'error',
              title: 'Please enter your contact number',
              confirmButtonColor: '#9fb300',
              timer: 4000
             })
    }

    else if(message == ''){
     Swal.fire({
              icon: 'error',
              title: 'Please enter your queries',
              confirmButtonColor: '#9fb300',
              timer: 4000
             })

    }

     else{

       let send_data = {
        name: name,
        email: email,
        phone: phone,
        message: message
        };

        let send_url = "http://127.0.0.1:8000/contact";
        $.ajax({
        type: "post",
        url: send_url,
        data: send_data,
        success : function (response){
            Swal.fire({
              icon: 'success',
              title: response.success,
              confirmButtonColor: '#9fb300',
              timer: 5000

             })
            $('form')[0].reset()
        },
        else:
        Swal.fire({
              icon: 'success',
              showConfirmButton: false,
              title: 'Sending Your Query'
             })

        })
     }

    })

});

// Application Form js
//$('#apply').on('click', function (e){
//           e.preventDefault();
//           let name = $('#id_name').val();
//           let email = $('#id_email').val();
//           let phone = $('#id_phone').val();
//           let position = $('#id_position').val();
//           photo = $('input[name=photo]').val();
//           cv = $('input[name=cv]').val();
//
//           let send_data = {
//            name: name,
//            email: email,
//            phone: phone,
//            photo: photo,
//            cv:cv,
//            position:position
//            };
//
//            let send_url = "http://127.0.0.1:8000/vacancy/vacancy-details/ ";
//            $.ajax({
//            type: "post",
//            url: send_url,
//            data: send_data,
//            success : function (response){
//                Swal.fire({
//                  icon: 'success',
//                  title: response.success,
//                  confirmButtonColor: '#9fb300',
//                  timer: 4000
//
//                 })
//                $('form')[0].reset()
//            },
//            else:
//            Swal.fire({
//                  icon: 'success',
//                  showConfirmButton: false,
//                  title: 'Sending Your Query'
//                 })
//
//            })
//
//
//
//        })
//
//
//
//
