/**
 * Created by Guanghui on 2017/5/11.
 */
'use strict';


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
    templateUrl: '/static/templates/exchcard/angular_templates/account-page.html'
  };

  var addressState = {
    url:'/address',
    name:'address',
    templateUrl:
      '/static/templates/exchcard/angular_templates/address-page.html'
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
      '/static/templates/exchcard/angular_templates/avatar-page.html'

  });


}]);

// app运行时
// app.run(function($rootScope, $http) {
//   var csrftoken = Cookies.get('csrftoken');
//
//   // 网络访问服务http
//   $http({
//     method: "GET",
//     headers: {
//       'X-CSRFToken': csrftoken
//     },
//     url: "/"
//   }).then(function mySucces(response) {
//
//   }, function myError(response) {
//
//   });
//
// });

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
    console.log(JSON.stringify(response.data));

    if (response.data != null){
      $scope.username = response.data.username;
      $scope.email = response.data.email;
    }



  }, function myError(response) {
    console.log(JSON.stringify(response));

  });

});


// 注册addressController
app.controller("addressController", function($scope, $http){
  // js.cookie可以产生csrftoken
  var csrftoken = Cookies.get('csrftoken');

  var urlPath = '/exchcard/api/address/get/info';

  $http({
    method:"GET",
    headers:{
      'X-CSRFToken': csrftoken
    },
    url: urlPath

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
  $("input.address-info-item-content").bind("input propertychange", function () {
    // console.log("address content changed!");

    // 按钮背景变化
    var b = $("button#save-address");
    b.addClass("active");
    b.prop('disabled', false);

    // 清除所有error message
    $(".error-message").text("");

  });

  $("#save-address").click(function(){
    console.log("clicked save address button!");

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
        console.log(JSON.stringify(response));

      }

    }).fail(function(response){
      console.log(JSON.stringify(response));
    });

  });




});




app.controller("avatarController", function($scope, $http) {
  // console.log("avatar ... ");

  // js.cookie可以产生csrftoken
  var csrftoken = Cookies.get('csrftoken');
  // 有关头像图片的URL
  var urlAvatarUrl = "/exchcard/api/profiles/avatar/url/";
  var urlUploadAvatar = "/exchcard/api/profiles/avatar/upload/";

  $http({
    method:"GET",
    headers:{
      'X-CSRFToken': csrftoken
    },
    url: urlAvatarUrl
  }).then(function mySucces(response) {
    console.log(JSON.stringify(response.data['avatar']));

    if (response.data.avatar != null){
      var avatarUrl = response.data['avatar'];
    }

  }, function myError(response) {
    // console.log(JSON.stringify(response));

  });


  $scope.upload_avatar = function(){

    console.log("upload avatar ... ");

    // 检测是否有文件
    var avatarInput = $("#avatar");
    if(avatarInput.val() === ''){
      console.log("avatar photo is empty!");
      $("span.errorMessage").text("头像图片不能为空!")
      return;
    }

    var formData = new FormData($( "#uploadAvatarForm" )[0]);
    $.ajax({
      url: urlUploadAvatar,
      type: 'POST',
      data: formData,
      async: false,
      cache: false,
      contentType: false,
      processData: false,
      success: function (returndata) {
        console.log(returndata);
      },
      error: function (returndata) {
        // console.log(returndata);
      }
    });

  }


});