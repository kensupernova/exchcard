/**
 * Created by Guanghui on 2016/12/13.
 */
$(document).ready(function() {

  //todo: 实时验证输入


  $("#btn-register-submit").click(function () {
    // get the input values for email and password
    var email = $("#form-email").val()|| "zgh1@126.com";
    var password = $("#form-password").val() ||"z111111";
    var username = email; // or randomly generated on server, turn email to hashcode

    var name = $("#form-name").val()|| "zgh";
    var address = $("#form-address").val() || "iamaddress";
    var postcode = $("#form-postcode").val() || "123445";


    // if(!validate_username(username)) {
    //   $("#email-error").text("错误");
    // }

    if(!validate_email(email)) {
      $("#email-error").text("邮箱地址错误");
      console.log(email);
      return;
    }
    if(!validate_password(password)) {
      $("#password-error").text("密码错误");
      console.log(password);
      return;
    }
    if(!validate_name(name)) {
      $("#name-error").text("姓名错误");
      console.log(name);
      return;
    }
    if(!validate_address(address)) {
      $("#address-error").text("邮寄地址错误");
      console.log(address);
      return;
    }
    if(!validate_postcode(postcode)) {
      $("#postcode-error").text("邮政编码错误");
      console.log(postcode);
      return;
    }



    var baseURL = "";
    var register_url = baseURL+"/exchcard/api/register/";

    console.log("register ...");

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
        url: register_url,
        data: {'username': username, 'password': password , "email": email,
        "name": name, "address": address, "postcode": postcode},
        success: function(data){
          console.log(data);
          // redirect to profile page
          window.location.href=baseURL +"/profile/"
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