/**
 *
 * Created by Guanghui on 2016/12/13.
 */
$(document).ready(function() {

  $("#btn-register-submit").click(function () {
    // get the input values for email and password
    var email = $("#form-email").val() || "zgh8@126.com";
    var password = $("#form-password").val() ||"z111111";

    // hashed username from email address
    var username = convert_email_to_username(email); // turn email to username by hashcode, hash-sha1-helper.js

    // console.log("new user name: " + username);

    var name = $("#form-name").val()|| "zgh";
    var address = $("#form-address").val() || "I am address 6";
    var postcode = $("#form-postcode").val() || "123445";


    if(!validate_email(email)) {
      $("#email-error").text("邮箱地址错误!");
      console.log(email);
      return;
    }

    if(!validate_password(password)) {
      $("#password-error").text("密码错误!");
      console.log(password);
      return;
    }

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
    var register_url = baseURL+"/exchcard/api/register/";

    console.log("register new profile...");

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
      data: {
        'username': username,
        'password': password ,
        "email": email,
        "name": name,
        "address": address,
        "postcode": postcode},
      success: function(data){
        // console.log("register successs!");

        // 同时login newly created user
        var id = setInterval(function () {
          var result = login_with_validated(username, password); // 函数来自login-helper.js
          if (result == 1){
            window.location.href = baseURL +"/profile/";
            clearInterval(id);
          } else {
            window.location.href = baseURL +"/register/";
          }
        }, 3000);

      }
    }).done(function(data){
      // console.log(JSON.stringify(data));

    }).fail(function(data){
      console.log(JSON.stringify(data['responseText']));
      console.log("register failed!");
    });
  });


});