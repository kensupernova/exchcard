/**
 * Created by Guanghui on 2017/5/17.
 */


function logout() {
  // console.log("log out ... ");
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

  $.ajax({
    method: "POST",
    url: url,
    success: function(data){
      // console.log("log out success!");

      // redirect to index page
      window.location.href= "/";
    }
  }).fail(function(){
    console.log("log out failed!");
  });

}

