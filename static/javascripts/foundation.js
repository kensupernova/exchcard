$(document).ready(function(){

  // local login
  $(".btn-login-submit").click(function(){
    // get the input values for email and password
    var email = $("#form_email").val()|| "zgh1@126.com";
    var password = $("#form_password").val()||"zz1111";

    // var email = $("#form_email").val();
    // var password = $("#form_password").val();

    console.log("password: " + password);
    console.log("email: " + email);

    if(!validate_email(email)){
      console.log("email is wrong")
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
        // console.log("login with email and password success!");
        result = 1;
        window.location.href = "/profile/";

      }
    }).fail(function(){
      console.log("login failed!");

      result = 0;
    });


  });

  // local logout
	$("#logout").click(function () {
	  console.log("log out ... ")
    var baseURL = "";
    var url = baseURL + "/exchcard/api/logout/";

    // csrf token
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    $.ajax({method: "POST",
      url: url,
      success: function(data){
        // redirect to profile page
        window.location.href= "/";
      }
    }).done(function(){
      // console.log("log out success!");
    }).fail(function(){
      // console.log("log out failed!");
    });

	});


  // 第1种方法html + js
  // WB2.anyWhere(function (W) {
  //   W.widget.connectButton({
  //     id: "wb_connect_btn",
  //     type: '3,2',
  //     callback: {
  //       login: function (o) { //登录后的回调函数
  //         alert("login: " + o.screen_name)
  //       },
  //       logout: function () { //退出后的回调函数
  //         alert('logout');
  //       }
  //     }
  //   });
  // });

  // 第二种方法WBML
  // 如需添加回调函数，请在wbml标签中添加onlogin="login" onlogout="logout"，并定义login和logout函数。
  // function login(o) {
  //   alert(o.screen_name)
  // }
  //
  // function logout() {
  //   alert('logout');
  // }

  // 3rd method login
  $("#wb_connect_btn").click(function () {
    window.location.href="/weibo/auth/";
  });

});



