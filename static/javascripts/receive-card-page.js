/**
 * Created by Guanghui on 2017/1/5.
 */
$(document).ready(function () {
  $("#submit").click(function () {
     receive_card();
  });


  function receive_card(){
    console.log("receive a card!");

    var receive_card_with_photo_url = "/exchcard/api/cards/receive/photo/";
    var receive_card_url = "/exchcard/api/cards/receive/";

    //// method 2
    // var form = $("#register-card-form");
    // form.action = url;
    // form.submit();

    //// 设置ajax
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

    console.log("recieve card submited data: " + card_name +" " + card_photo);

    var formData;

    if(!card_photo || card_photo == null || card_photo == undefined){
      console.log("card photo is empty!")

      var formData = {
        card_name: card_name,
      }

      // console.log("submit data  "+JSON.stringify(formData));

      $.ajax({
        method:"post",
        url: receive_card_url,
        data: formData,
        success: function(data){
          console.log("receive card success : " + JSON.stringify(data));

          // redirect to profile page
          window.location.href=  "/profile/"
        }

      }).done(function(data){
        // console.log("receive card success : " + JSON.stringify(data));

      }).fail(function(data){
        console.log(JSON.stringify(data));

        console.log("receive card failed!");
      });

    } else{
      ///////// 带图片的明信片
      var formData = {
        card_name: card_name,
        card_photo: card_photo
      }

      // console.log("submit data  "+JSON.stringify(formData));

      $.ajax({
        method:"post",
        url: receive_card_with_photo_url,
        data: formData,
        enctype: 'multipart/form-data',
        success: function(data){
          console.log("receive card success : " + JSON.stringify(data));

          // redirect to profile page
          window.location.href=  "/profile/"
        }

      }).done(function(data){
        // console.log("receive card success : " + JSON.stringify(data));

      }).fail(function(data){
        console.log(JSON.stringify(data));
        console.log("receive card failed!");
      });

    }


  }


  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }


});