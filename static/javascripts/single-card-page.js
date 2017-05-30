/**
 * Created by Guanghui on 2017/5/29.
 */

$("#upload-btn").click(function(){

  console.log("uploading card photo ...");

  var card_photo = $("#card_photo_file").val();
  var card_name = $("#post-cardname-holder").text();

  if(card_photo== null || !card_photo || card_photo == undefined) return;


  var formData = new FormData();
  formData.append('card_photo', $("#card_photo_file")[0].files[0]);
  formData.append('card_name', card_name);

  addCSRFTokenBeforeAjax();

  var upload_photo_afterwards_url = "/exchcard/api/cards/"+ card_name + "/upload/photo/";

  $.ajax({
    url: upload_photo_afterwards_url,
    type: 'POST',
    data: formData,
    dataType: 'json',
    async: false,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      // console.log("upload photo success: " + JSON.stringify(response));

      var ele = '<div><img src="' + response['card_photo_url'] + '"></div>';

      $("div#card-photos-container").append(ele);

      // 显示成功发送
      $("#upload-result-msg").text("成功上传图片!");
      setTimeout(function () {
        $("#upload-result-msg").hide();
      }, 5000)
    },
    error: function (response) {
      // console.log(JSON.stringify(response));
      // console.log("receive card failed!");

      $("#upload-error-msg").text(response["responseJSON"]["details"]);
    }
  });

  // var formData;
  //
  // formData = {
  //   card_name: card_name,
  //   card_photo: card_photo
  // };
  //
  // addCSRFTokenBeforeAjax();
  //
  // var upload_photo_afterwards_url = "/exchcard/api/cards/"+ card_name + "/upload/photo/";
  //
  // $.ajax({
  //   method:"post",
  //   url: upload_photo_afterwards_url,
  //   data: formData,
  //   enctype: 'multipart/form-data',
  //   success: function(response){
  //     console.log("upload photo success: " + JSON.stringify(response));
  //
  //     // 显示成功发送
  //     $("#upload-result-msg").text("成功上传图片!");
  //
  //   }
  //
  // }).fail(function(response){
  //   console.log(JSON.stringify(response));
  //   // console.log("receive card failed!");
  //
  //   $("#upload-error-msg").text(response["responseJSON"]["details"]);
  // });
  //


});






