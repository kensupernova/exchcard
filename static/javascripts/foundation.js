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
        // redirect to profile page
        window.location.href= "/";
      }
    }).done(function(){
      console.log("log out success!");
    }).fail(function(){
      console.log("log out failed!");
    });

	});

  $("#setting").click(function () {
    console.log("go to settting ... ");
    window.location.href= "/account/setting";

  });



});



