$(document).ready(function(){

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
          // console.log(data);
          // redirect to profile page
          window.location.href= "/";
        }
      }
    ).done(function(){
      console.log("success!");
    }).fail(function(){
      console.log("failed!");
    });

	});



});



