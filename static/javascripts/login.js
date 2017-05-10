$(document).ready(function(){

  // local login
	$(".btn-login-submit").click(function(){
		// get the input values for email and password
		var email = $("#form_email").val()|| "zgh8@126.com";
		var password = $("#form_password").val()||"z111111";

		var username = convert_email_to_username(email);

    // console.log("username: " + username);
    // console.log("password: " + password);
    // console.log("email: " + email);

		if(!validate_username(username)){
		  console.log("username is wrong")
			return;
		}

		if(!validate_password(password)){
      console.log("password is wrong")
			return;
		}


		// use api for login
		var baseURL = "";
		var login_url = baseURL + "/exchcard/api/login/";

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
      url: login_url,
			data: {'username': username, 'password':password},
			success: function(data){
					// console.log(data);
					// redirect to profile page
					window.location.href=baseURL +"/profile/"
      }

		}).done(function(){
			console.log("log in success!");

		}).fail(function(){
			console.log("log in failed!");
		});


	});

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}


  //// 微博登录
  //// HTML + JS
  // WB2.anyWhere(function(W){
  //     W.widget.connectButton({
  //         id: "wb_connect_btn",
  //         type:"1,1",
  //         callback : {
  //             login:function(o){	//登录后的回调函数
  //             },
  //             logout:function(){	//退出后的回调函数
  //             }
  //         }
  //     });
  // });
  //


});

