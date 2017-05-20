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

  // 当点击微博开放平台退出
  //第二种方法html + js
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

});



