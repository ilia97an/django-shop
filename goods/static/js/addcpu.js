//2023sep18 02:16!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//it worked!
$(document).ready(function(e) {
//  $('#submit').on('click', function (event) {
  $('#form').submit(function(event) {
    event.preventDefault();
    /*//var form_data = new FormData($('#form')[0]);
    const form_data = new FormData();
    var name = $('#id_name').val();
    //console.log(typeof(name));
    form_data.append("name", name);
    var price = $('#id_price').val();
    form_data.append("price", price);
    // check if there is any file selected
    
    var ins = $('#id_images')[0].files.length;
    //add all files
    //for (var x = 0; x < ins; x++) {
    //  //document.getElementById
    //  form_data.append("files[]", $('id_images')[0].files[x])
    //}
    for ([key, value] of form_data) {
      console.log(key, value);
    }*/
    //obtain CSRF token
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    
    //set the headers
    //var headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest', 'X-CSRFToken': csrf_token};
    //var headers = {'X-CSRFToken': csrf_token};
    $.ajax({
      type: 'POST',
      url: '/goods/addcpu/', //point to server-side URL
      dataType: "json",
      //ContentType: 'application/x-www-form-urlencoded',
      cache: false,
      contentType: false,
      //contentType: 'multipart/form-data',
      processData: false,
      //enctype: 'multipart/form-data',
      //enctype: , 
      headers: {'X-CSRFToken': csrf_token},
      //data: {'name': name, 'price': price, form_data},
      //data: form_data,
      //data: $('#form').serialize(),
      data: new FormData($('#form')[0]),
      success: function (response) { //display success response
        console.log('sucesssssssssssssss');
        console.log(response.answer);
      },
      error: function(response) {
        console.log('noooooooooope');
        console.log(response.answer);
      }
    });
    return false;
  });
});

