/**
 * Created by Guanghui on 2017/5/11.
 */
'use strict';

// var baseUrl = window.location.origin ;
var baseUrl = window.location.protocol +"//"+window.location.host;

// Use angular ui router to achieve tabs, add ui.router as module dependency
var app = angular.module('myApp', ['ui.router']);

// 修改angular的标签
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});


app.config(["$stateProvider", "$urlRouterProvider", function ($stateProvider, $urlRouterProvider) {

  // Setup router
  $urlRouterProvider.when("", "/account").otherwise('/');

  var accountState = {
    url:'/account',
    name:'account',
    templateUrl: '/static/templates/exchcard/angular_templates/settings/account-page.html'
  };

  var addressState = {
    url:'/address',
    name:'address',
    templateUrl:
      '/static/templates/exchcard/angular_templates/settings/address-page.html'
  };

  // 注册各个状态
  $stateProvider
    .state(accountState)
    .state(addressState);

  // Second method to register state
  $stateProvider.state('avatar', {
    url:'/avatar',
    name:'avatar',
    templateUrl:
      '/static/templates/exchcard/angular_templates/settings/avatar-page.html'

  });


}]);


// 注册accountController
app.controller("accountController", function($scope, $http){

  var csrftoken = Cookies.get('csrftoken');

  var urlPath = '/exchcard/api/users/get/info/';

  $http({
    method:"GET",
    headers:{
      'X-CSRFToken': csrftoken
    },
    url: urlPath

  }).then(function mySucces(response) {
    // console.log(JSON.stringify(response.data));

    if (response.data != null){
      $scope.username = response.data.username;
      $scope.email = response.data.email;
    }

  }, function myError(response) {
    console.log(JSON.stringify(response));

  });


  // 监控用户名的变化
  $("#username").bind("input propertychange", function () {
    $("#btn-username-save").show();
    // var elem = $("#username");
    // alert('你改变了用户名!' + elem.val());
    // 再服务器上
  });

  // 在服务器上更新用户名。
  $scope.updateUsername = function(){
    var new_username = $("#username").val();
    if(!new_username || new_username == null || new_username == undefined){
      return;
    }

    var update_username_url = "/exchcard/api/users/update/username/";

    var data = {"username": new_username};

    // addCSRFTokenBeforeAjax();
    var csrftoken = Cookies.get('csrftoken');

    $http({
      method: "POST",
      url:update_username_url,
      headers:{
        'X-CSRFToken': csrftoken
      },
      data: data
    }).then(function mySucess(response){
        // alert("update success");
        // console.log(JSON.stringify(response));
        $("#btn-username-save").hide();
        $("#username-error-msg").text("成功修改该用户名!").show();
        // $("#username-error-msg").show();

        setTimeout(function(){
          $("#username-error-msg").fadeOut(1000);
        }, 3000);

    },
      function myError(response) {
        // console.log(JSON.stringify(response));
        $("#username-error-msg").text(response["responseJSON"]["details"]);
    });

  };

  //-----------------
  // 监控旧密码输入的变化
  $("input#password-old").change(function () {
    // alert("输入完, 失去焦点。");
    var pwd_old = $("#password-old").val();
    // console.log("pwd old is " + pwd_old);

    // 显示查询loading animation
    $("#loader").show();

    // check with server
    var check_pwd_url = "/exchcard/api/users/check/password/";
    var csrftoken = Cookies.get('csrftoken');
    $http({
      method: "POST",
      url:check_pwd_url,
      headers:{
        'X-CSRFToken': csrftoken
      },
      data: {
        "password": pwd_old
      }
    }).then(function mySucess(response){
      // alert("update success");
      // console.log(JSON.stringify(response));
      var is_correct = response.data['is_correct'];

      $("#loader").hide();

      if(is_correct || is_correct == 1 || is_correct == '1'){
        $("#pwd-old-error-msg").text("密码正确").show();
      } else{
        $("#pwd-old-error-msg").text("密码错误").show();

        // 移动光标到旧密码后面
        var e = $("#password-old");
        e.focus();
        var r =e.createTextRange();
        r.moveStart('character',e.value.length);
        r.collapse(true);
        r.select();
      }

    },
      function myError(response) {
        // console.log(JSON.stringify(response));
        $("#pwd-old-error-msg").text(response["responseJSON"]["details"]);
    }
    );

  });


  $scope.confirmChangePwd = function () {
    var password = $("#password-new").val() ;
    var password2 = $("#password-new-2").val() ;

    if(password2!=password){
      $("#password-error-2").text("第二次输入秘密与第一次不一致。")
      return false;
    }

    if(!validate_password(password)) {
      $("#password-error").text("密码不满足要求!");
      return false;
    }

    // console.log("update pwd "+ password +", " + password2);
    // check with server
    var update_pwd_url = "/exchcard/api/users/update/password/";
    var csrftoken = Cookies.get('csrftoken');
    $http({
      method: "POST",
      url: update_pwd_url,
      headers:{
        'X-CSRFToken': csrftoken
      },
      data: {
        "new_password": password
      }
    }).then(function mySucess(response){

      // alert("update success");
      console.log(JSON.stringify(response.data));
      var isSuccess = response.data["update_pwd_is_succuss"];
      // var isSuccessInt = response.data["update_pwd_is_succuss_int"];
      if(isSuccess || isSuccess == 1 || isSuccess == '1'){
        window.location.href = "/account/login/";
      }

      },
      function myError(response) {
        // console.log(JSON.stringify(response));
      }
    );

  }

});


// 注册addressController
app.controller("addressController", function($scope, $http){
  // js.cookie可以产生csrftoken
  var csrftoken = Cookies.get('csrftoken');

  var getAddressUrl = '/exchcard/api/address/get/info';

  $http({
    method:"GET",
    headers:{
      'X-CSRFToken': csrftoken
    },
    url: getAddressUrl

  }).then(function mySucces(response) {
    // console.log(JSON.stringify(response.data));

    if (response.data != null){
      $scope.name = response.data['name'];
      $scope.address = response.data['address'];
      $scope.postcode = response.data['postcode'];
    }



  }, function myError(response) {
    console.log(JSON.stringify(response.data));

  });

  // 监听input.address-info-item-content的内容改变
  $(".address-info-item-content").bind("input propertychange", respond_to_address_change);

  function respond_to_address_change() {
      // console.log("address content changed!");

      // 按钮背景变化, 激活按钮
      var b = $("button#save-address");
      b.addClass("active");
      b.prop('disabled', false);

      // 清除所有error message
      $(".error-message").text("");
  }



  $("#save-address").click(function(){
    // console.log("clicked save address button!");

    var newName = $("#name").val();
    var newAddress = $("#address").val();
    var newPostcode = $("#postcode").val();

    if(!validate_name(newName)) {
      $("#name-error").text("姓名错误! 要求:2-10位汉字；3-30位字母; 可以包括空格,点号");
      return false;
    }

    if(!validate_address(newAddress)) {
      $("#address-error").text("邮寄地址错误! 要求:2-50位汉字; 5-100位字母");
      return false;
    }


    if(!validate_postcode(newPostcode)) {
      $("#postcode-error").text("邮政编码错误! ");
      return false;
    }

    var updateAddressUrl = "/exchcard/api/address/update/";

    var data = {
      name: newName,
      address: newAddress,
      postcode: newPostcode
    };

    // setting csrf token, 避免403错误
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    $.ajax({
      method: "post",
      url: updateAddressUrl,
      data: data,
      success: function(response){
        // console.log(JSON.stringify(response));

        // 按钮背景变化, disable按钮
        var b = $("button#save-address");
        b.removeClass("active");
        b.prop('disabled', true);

        // 清除所有error message
        $(".error-message").text("");

      }

    }).fail(function(response){
      console.log(JSON.stringify(response));
    });

  });


});


// -----------------------------------------------------------

app.controller("avatarController", function($scope, $http) {
  // console.log("avatar ... ");

  // var baseUrl = window.location.origin ;
  var baseUrl = window.location.protocol +"//"+window.location.host;
  var defaultAvatarUrl = "/static/images/default-avatar.jpg";

  // 有关头像图片的URL
  var getAvatarUrl = "/exchcard/api/profiles/avatar/url/";
  var uploadAvatarUrl = "/exchcard/api/profiles/avatar/upload/";


  // js.cookie可以产生csrftoken
  var csrftoken = Cookies.get('csrftoken');


  // 下载头像图片
  $http({
    method:"GET",
    headers:{
      'X-CSRFToken': csrftoken
    },
    url: getAvatarUrl
  }).then(function mySucces(response) {

    // method 2
    var avatar_url= response.data['avatar_url'];
    if(avatar_url != null){
      $scope.avatar_url = avatar_url;
    } else{
      $scope.avatar_url = baseUrl + defaultAvatarUrl;
    }


  }, function myError(response) {
    // console.log(JSON.stringify(response));

  });

  //// 上传avatar photo
  $scope.upload_avatar = function(){

    // console.log("upload avatar ... useing ajax + FormData ");

    // 检测是否有文件
    var avatarInput = $("#avatar");

    if(avatarInput.val() === ''){
      // console.log("avatar photo input is empty!");
      $(".form-row>div .errorMessage").show();
      return;
    } else {
      $(".form-row>div .errorMessage").hide();
    }

    // method 2
    // var file=$("#avatar")[0].files[0];
    // if(file==null)
    //   return;
    // var formData=new FormData();
    // formData.append('avatar',file);

    var formData = new FormData($("#uploadAvatarForm")[0]);

    // 在ajax前, 添加csrftoken
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    $.ajax({
      url: uploadAvatarUrl,
      type: 'POST',
      data: formData,
      dataType: 'json',
      async: false,
      cache: false,
      contentType: false,
      processData: false,
      success: function (response) {
        // console.log("after uploading " + JSON.stringify(response));
        $("#avatar").empty();

        $scope.avatar_url = response['avatar'];

      },
      error: function (response) {
        // console.log(response);
      }
    });

  }


});