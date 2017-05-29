/**
 *
 * Created by Guanghui on 2016/12/13.
 */
$(document).ready(function() {

  $("#btn-register-submit").click(function () {
    // get the input values for email and password
    // var email = $("#form-email").val() || "zgh8@126.com";
    // var password = $("#form-password").val() || "z111111";
    // var password2 = $("#form-password-2").val() ||  "z111111";

    var email = $("#form-email").val() ;
    var password = $("#form-password").val() ;
    var password2 = $("#form-password-2").val() ;

    if(password2!=password){
      $("password-error-2").text("第二次输入秘密与第一次不一致。")
      return false;
    }

    // hashed username from email address
    // var username = convert_email_to_username_fool(email); // turn email to username, hash-sha1-helper.js
    var username = convert_email_to_username_sha1(email);

    // console.log("new user " + username +" " + email +" " + password);


    if(!validate_email(email)) {
      $("#email-error").text("邮箱地址格式错误!");
      console.log(email);
      return;
    }

    if(!validate_password(password)) {
      $("#password-error").text("密码不满足要求!");
      console.log(password);
      return;
    }


    var baseURL = "";
    var register_url = baseURL+"/exchcard/api/users/register/";

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
        "email": email
      },
      success: function(data){
        //console.log("register new user successs!");

        // 同时login newly created user
        var login_url = "/exchcard/api/login/";

        // 设置csrf token
        var csrftoken = Cookies.get('csrftoken');

        $.ajaxSetup({
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          }
        });

        var result = 0;

        // 发动登录请求
        $.ajax({
          method: "POST",
          url: login_url,
          data: {'email': email, 'password':password},
          success: function(data){
            // console.log("log in after register success!");

            result = 1;

            window.location.href = "/account/address/create/";
          }
        }).fail(function(){
          console.log("login failed!");

          result = 0;
        });

      }


    }).done(function(data){
      // console.log(JSON.stringify(data));

    }).fail(function(data){
      console.log("register failed!");
      console.log(JSON.stringify(data['responseJSON']));

      var response = data["responseJSON"];
      // 得到Error Message
      var errorMessage = response['email'];
      $("#server-error-message").text(errorMessage)

    });


  });


});