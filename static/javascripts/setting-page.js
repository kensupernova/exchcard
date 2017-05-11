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

  // // Second method to create state
  // $stateProvider.state('avatar', {
  //   url:'/avatar',
  //   name:'avatar',
  //   templateUrl:
  //     '/static/templates/exchcard/angular_templates/avatar-page.html'
  //
  // });


}]);


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
