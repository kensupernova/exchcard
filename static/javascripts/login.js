$(document).ready(function(){

  // local login
	$(".btn-login-submit").click(function(){
    // get the input values for email and password
    var email = $("#form_email").val()|| "zgh1@126.com";
    var password = $("#form_password").val()||"z111111";

    // var email = $("#form_email").val();
    // var password = $("#form_password").val();

    var username = convert_email_to_username(email);

    // console.log("username: " + username);
    // console.log("password: " + password);
    // console.log("email: " + email);

    if(!validate_email(email)){
      console.log("email is wrong")
      return;
    }

    if(!validate_username(username)){
      console.log("username is wrong")
      return;
    }

    if(!validate_password(password)){
      console.log("password is wrong")
      return;
    }

    // use api for login
    var baseURL = "";
    var login_url = baseURL + "/exchcard/api/login/";

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
        console.log("login success!");
        result = 1;
        window.location.href = "/profile/";

      }
    }).fail(function(){
      console.log("login failed!");

      result = 0;
    });


	});


  //// 微博登录
  //// HTML + JS
  // WB2.anyWhere(function(W){
  //     W.widget.connectButton({
  //         id: "wb_connect_btn",
  //         type:"1,1",
  //         callback : {
  //             login:function(o){	//登录后的回调函数
  //             },
  //             logout:function(){	//退出后的回调函数
  //             }
  //         }
  //     });
  // });
  //


});

