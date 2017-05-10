/**
 * Created by Guanghui on 2017/5/10.
 */

function login_with_validated(username, password){
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


  // 发动登录请求
  $.ajax({method: "POST",
      url: login_url,
      data: {'username': username, 'password':password},
      success: function(data){
        // console.log(data);
        // redirect to profile page
        window.location.href=baseURL +"/profile/"
      }
    }
  ).done(function(){
    console.log("login success!");

    return 1;
  }).fail(function(){
    console.log("login failed!");

    return 0;
  });

}