/**
 * Created by Guanghui on 2016/12/17.
 */

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function addCSRFTokenBeforeAjax(){
  // csrf token
  // 解决403错误, 发送ajax post请求前, 添加X-CSRFTOKEN HEADER
  // 基于 js.cookie.js
  var csrftoken = Cookies.get('csrftoken'); // 发送请求时,提取csrftoken cookie
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  // 相当于
  //      var csrftoken = Cookies.get('csrftoken');
  //      headers: {
  //        'X-CSRFToken': csrftoken
  //      }
}