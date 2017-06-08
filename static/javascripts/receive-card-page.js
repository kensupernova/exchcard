/**
 * Created by Guanghui on 2017/1/5.
 */

$(document).ready(function () {

  $("#cards").addClass('active');


  $("#btn-submit").click(function () {
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
    var input_card_photo = $("#card_photo");
    var card_photo = input_card_photo.val();

    if(!card_name || card_name == '' || card_name == null || card_name == undefined){
      alert("未填写注册明信片的Postcard Id!");
      return;
    }



    ///// 分两种情况讨论。
    if(!card_photo || card_photo == null || card_photo == undefined){
      // console.log("card photo is empty!");

      // console.log("submit data  "+JSON.stringify(formData));
      var data = {
        card_name: card_name,
      };

      $.ajax({
        method:"post",
        url: receive_card_url,
        data: data,
        success: function(data){
          console.log("receive card success with no photo: " + JSON.stringify(data));

          // 显示成功发送
          $("#receive-card-result").text("成功注册明信片!");

          // redirectToProfile();
          redirectToSingleCardPage(card_name);
        }

      }).fail(function(data){
        // console.log(JSON.stringify(data));
        // console.log("receive card failed!");
        $("#receive-card-result-details").text(data["responseJSON"]["details"]);
        $("#receive-card-result-msg").text("注册明信片失败!")

      });

    } else{
      ///////// 带图片的明信片

      var formData = new FormData();

      formData.append("card_name", card_name);
      formData.append("card_photo", input_card_photo[0].files[0]);

      // console.log("submited data  "+JSON.stringify(formData));

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
          // redirectToProfile();
          redirectToSingleCardPage(card_name);

        }
      }).fail(function(data){
        // console.log(JSON.stringify(data));
        // console.log("receive card failed!");

        $("#receive-card-result-details").text(data["responseJSON"]["details"]);
        $("#receive-card-result-msg").text("注册明信片失败!")

      });

    }


  }

  function redirectToProfile(){
    // 2s后,挑转
    setTimeout(function(){
      // redirect to profile page
      window.location.href=  "/profile/"
    }, 2000);
  }

  function redirectToSingleCardPage(card_name){
    // 2s后,挑转
    setTimeout(function(){
      // redirect to profile page
      window.location.href=  "/card/" + card_name;
    }, 2000);
  }


});