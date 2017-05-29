/**
 * Created by Guanghui on 2017/1/5.
 */

$(document).ready(function () {

  $("#cards").addClass('active');


  $("#submit").click(function () {
     receive_card();
  });


  function receive_card(){

    var receive_card_with_photo_url = "/exchcard/api/cards/receive/photo/";
    var receive_card_url = "/exchcard/api/cards/receive/";

    //// 设置ajax csrf
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

    if(!card_name || card_name == '' || card_name == null || card_name == undefined){
      return;
    }

    ///// 分两种情况讨论。
    if(!card_photo || card_photo == null || card_photo == undefined){
      // console.log("card photo is empty!");

      var formData = {
        card_name: card_name,
      };

      // console.log("submit data  "+JSON.stringify(formData));

      $.ajax({
        method:"post",
        url: receive_card_url,
        data: formData,
        success: function(data){
          console.log("receive card success with no photo: " + JSON.stringify(data));

          // 显示成功发送
          $("#receive-card-result").text("成功注册明信片!");

          redirectToProfile();
        }

      }).fail(function(data){
        // console.log(JSON.stringify(data));
        // console.log("receive card failed!");
        $("#receive-card-result").text(data["responseJSON"]["details"]);
        redirectToProfile();
      });

    } else{

      ///////// 带图片的明信片
      var formData = new FormData();

      formData.append("card_photo", $("#card_photo")[0].files[0]);
      formData.append('card_name', card_name);

      // console.log("submit data  "+JSON.stringify(formData));

      $.ajax({
        url: receive_card_with_photo_url,
        type: 'POST',
        data: formData,
        dataType: 'json',
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data){
          console.log("receive card success with photo: " + JSON.stringify(data));

          // 显示成功发送
          $("#receive-card-result").text("成功注册明信片");

          // 2s后,挑转
          redirectToProfile();


        },
        error: function (data) {

        }

      }).fail(function(data){
        // console.log(JSON.stringify(data));
        // console.log("receive card failed!");
        $("#receive-card-result").text(data["responseJSON"]["details"]);

        redirectToProfile();

      });

    }


  }

  function redirectToProfile(){
    // 5s后,挑转
    setTimeout(function(){
      // redirect to profile page
      window.location.href=  "/profile/"
    }, 2000);
  }


  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }


});