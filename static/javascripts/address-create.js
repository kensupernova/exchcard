/**
 *
 * Created by Guanghui on 2016/12/13.
 */
$(document).ready(function() {

  $("#btn-register-submit").click(function () {

    // var name = $("#form-name").val()|| "zgh7";
    // var address = $("#form-address").val() || "address street 1, Chengdu, China";
    // var postcode = $("#form-postcode").val() || "610234";

    var name = $("#form-name").val();
    var address = $("#form-address").val();
    var postcode = $("#form-postcode").val();

    if(!validate_name(name)) {
      $("#name-error").text("姓名错误!");
      console.log(name);
      return;
    }

    if(!validate_address(address)) {
      $("#address-error").text("邮寄地址错误!");
      console.log(address);
      return;
    }


    if(!validate_postcode(postcode)) {
      $("#postcode-error").text("邮政编码错误!");
      console.log(postcode);
      return;
    }


    var baseURL = "";
    var address_create_url = baseURL+"/exchcard/api/address/profile/create/";

    // console.log("register new address...");

    // csrf token, 避免403错误
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    $.ajax({
      method:"post",
      url: address_create_url,
      data: {
        "name": name,
        "address": address,
        "postcode": postcode
      },
      success: function(data){
        console.log("address register successs! profile create successs!");

        // 3秒钟内,跳转到个人主页
        var id = setInterval(function () {

            window.location.href = baseURL +"/profile/";
        }, 1000);

      }
    }).fail(function(data){
      console.log(JSON.stringify(data['responseText']));
      console.log("register address profile failed!");
    });
  });


});