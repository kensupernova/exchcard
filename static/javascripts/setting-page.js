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
    console.log(JSON.stringify(response.data));

    if (response.data != null){
      $scope.name = response.data['name'];
      $scope.address = response.data['address'];
      $scope.postcode = response.data['postcode'];
    }



  }, function myError(response) {
    console.log(JSON.stringify(response));

  });


});