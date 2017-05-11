$(document).ready(function(){

  // 当点击退出按钮时
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

  // 当点击设置按钮时
  $("#setting").click(function () {
    console.log("go to settting page ... ");
    window.location.href= "/setting";

  });



});



