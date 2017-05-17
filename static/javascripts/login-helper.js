/**
 * 本地登录
 * 微博登录
 * Created by Guanghui on 2017/5/10.
 */

function login_with_validated(email, password){
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
      result = 1;
      console.log("log in by login-helper.js success!");

    }
  }).fail(function(){
    console.log("login failed!");

    result = 0;
  });

  return result;
}