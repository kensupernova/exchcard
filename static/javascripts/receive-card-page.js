/**
 * Created by Guanghui on 2017/1/5.
 */
$(document).ready(function () {
  $("#submit").click(function () {
    console.log("clicked submit button");

    var url = "/exchcard/api/cards/receive/photo/";
    //
    // var form = $("#register-card-form");
    //
    // form.action = url;
    //
    // form.submit();


    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    var card_name = $("#card_name").val();
    var card_photo = $("#card_photo").val();


    formData = {
      card_name: card_name,
      card_photo: card_photo
    }

    console.log(JSON.stringify(formData));

    $.ajax({
        method:"post",
        url: url,
        data: formData,
        enctype: 'multipart/form-data',
        success: function(data){
          console.log(data);
          // redirect to profile page
          window.location.href=  "/profile/"
        }
      }
    ).done(function(data){
    }).fail(function(data){
      console.log(data);
      console.log("failed!");
    });
  });

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }




});