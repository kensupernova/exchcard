/**
 * Created by Guanghui on 2017/5/26.
 */
(function(){
  $("#cards").addClass('active');

  // 点击上传按钮
  $("#btn-upload-card-photo").click(function () {

    console.log("uploading card photo on travelling card page ...");

    var input_card_photo = $("#card_photo_file");

    // 如果没有文件, 就返回
    var card_photo = input_card_photo.val();
    if(card_photo== null || !card_photo || card_photo == undefined){
      $("#upload-result-msg").text("没有文件!");
      return;
    } else{
      $("#upload-result-msg").text("");
    }

    var card_photo_file = input_card_photo[0].files[0];

    var card_name = $("#card-name-holder").text();

    var formData = new FormData();

    formData.append('card_photo', card_photo_file);
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

        var ele = '<div><img src="' + response['card_photo']['card_photo_url'] + '"></div>';

        $("div#card-photos-container").append(ele);

        // 显示成功发送
        $("#upload-result-msg").text("成功上传图片!");
        input_card_photo.val('');

        // 3s后, 上传结果信息自动消失
        setTimeout(function () {
          // $("#upload-result-msg").hide();

        }, 2000);

      },
      error: function (response) {
        // console.log(JSON.stringify(response));
        // console.log("receive card failed!");

        $("#upload-result-msg").text("上传图片失败!");
        // 3s后, 上传结果信息自动消失
        setTimeout(function () {
          // $("#upload-result-msg").hide();

        }, 2000);

      }
    });

  });


})();

