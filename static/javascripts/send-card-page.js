$(document).ready(function(){

  $("#cards").addClass('active');

  // 预先新明信片的地址信息
  // 预先新明信片的card_name
  var pre_card_address = null;
  var pre_card_name = null;


  $("#btn-get-address").click(function () {
    // 确保 checkbox已经打钩
    if(!$("#check-confirm-warning").prop("checked")){
      alert("先确认阅读了警告文字!");
      return;
    }

    var getAddress = "/exchcard/api/"+'cards/get/address/';

    // var csrftoken = Cookies.get('csrftoken');
    // headers: {
    //   'X-CSRFToken': csrftoken
    // },

    $.ajax({
      method: "GET",
      url: getAddress,
      success: function mySucces(response) {
        // console.log(JSON.stringify(response));

        // FILL IN DATA
        if(response != null){

          // 成功得到地址后, 显现转, 隐藏注意事项
          var block1 = $("#sent-warning-container");
          block1.removeClass("shown-content");
          block1.addClass("hidden-content");

          var block2 = $("#create-card-container");
          block2.addClass("shown-content");
          block2.removeClass("hidden-content");


          pre_card_address = response;
          pre_card_name = response.card_name;

          $("#torecipient-id-holder").text(pre_card_address.torecipient_id);
          $("#card-name-holder").text(pre_card_address.card_name);
          $("#postal-name-holder").text(pre_card_address.name);
          $("#postal-address-holder").text(pre_card_address.address);
          $("#postal-postcode-holder").text(pre_card_address.postcode);
          $("#postal-country-holder").text(pre_card_address.country);

        }

      },
      error: function myError(response) {
        // console.log(JSON.stringify(response));

      }
    });
  });

  // 用户确定发送明信片
  $("#btn-confirm-send-card").click(function () {
    if(!$("#check-confirm-send").prop("checked")){
      alert("至少要确认发送明信片!");
      return;
    }

    if(pre_card_address == null || pre_card_name == null){
      alert("还未得到明信片ID和地址!");
      return;
    }

    var data = pre_card_address;

    var has_photo = $("#check-has-photo").prop("checked"); // boolean
    var has_photo_int = Number(has_photo);

    if(has_photo || has_photo_int == 1){
      alert("你将上传明信片图片");
    }

    var input_card_photo = $("#card_photo_file");

    if(has_photo || has_photo_int == 1){
      var card_photo = input_card_photo.val();

      if(card_photo == null || !card_photo || card_photo == undefined) {
        has_photo = false;
        has_photo_int = 0;

        alert("没有明信片图片");
        return;
      }
    }

    data["has_photo"] = has_photo;
    data["has_photo_int"] = has_photo_int;

    // console.log("data before ajax: " + JSON.stringify(data));

    var csrftoken = Cookies.get('csrftoken');
    var path = "/exchcard/api/cards/confirm/send/card/";
    var pathPhoto = "/exchcard/api/cards/confirm/send/card/";

    // 如果有图片
    if(has_photo || has_photo_int == 1){
      var formData = new FormData();

      for ( var key in data ) {
        if(data.hasOwnProperty(key)){
          formData.append(key, data[key]);
        }
      }

      // TESTING
      // var data = {
      //   a: "1",
      //   b: "2",
      //   c: "3"
      // };
      //
      // for ( var key in data ) {
      //   if(data.hasOwnProperty(key)){
      //     console.log(data[key])
      //   }
      // }

      var card_photo_file = input_card_photo[0].files[0];
      formData.append('card_photo', card_photo_file);

      $.ajax({
        url: pathPhoto,
        headers: {
          'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: formData,
        dataType: 'json',
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
          // console.log(JSON.stringify(response));

          $("#send-card-result-msg").text("成功,有图片!");
          // 3s后, 上传结果信息自动消失
          setTimeout(function () {
            $("#send-card-result-msg").hide();

            window.location.href = "/card/travelling/" + pre_card_name;
          }, 3000);


        },
        error: function (response) {
          // console.log(JSON.stringify(response));

          $("#send-card-result-msg").text("失败!");
          // 3s后, 上传结果信息自动消失
          setTimeout(function () {
            $("#send-card-result-msg").hide();
          }, 3000);
        }
      });

    }
    else {

      $.ajax({
        method: "POST",
        url: path,
        data: data,
        headers: {
          'X-CSRFToken': csrftoken
        },
        success: function mySucces(response) {
          // console.log(JSON.stringify(response));

          $("#send-card-result-msg").text("成功,无图片!");
          // 3s后, 上传结果信息自动消失


          setTimeout(function () {
            $("#send-card-result-msg").hide();

            window.location.href = "/card/travelling/" + pre_card_name;
          }, 3000);


        },
        error: function myError(response) {
          // console.log(JSON.stringify(response));

          $("#send-card-result-msg").text("失败!");
          // 3s后, 上传结果信息自动消失
          setTimeout(function () {
            $("#send-card-result-msg").hide();
          }, 3000);

        }
      });

    }


  });



});




