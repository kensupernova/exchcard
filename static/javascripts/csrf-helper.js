/**
 * Created by Guanghui on 2016/12/17.
 */

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// // csrf token
// var csrftoken = Cookies.get('csrftoken');
// $.ajaxSetup({
//   beforeSend: function(xhr, settings) {
//     if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//       xhr.setRequestHeader("X-CSRFToken", csrftoken);
//     }
//   }
// });