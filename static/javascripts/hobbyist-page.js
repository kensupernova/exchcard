/**
 * Created by Guanghui on 2017/5/22.
 */
// var baseUrl = window.location.origin ;
var baseUrl = window.location.protocol +"//"+window.location.host;

var baseUrl2 = window.location.protocol +"//"+window.location.host+":"+window.location.port

$(document).ready(function(){
  $("#hobbyist").addClass('active');

  // $(".h-item").click(function () {
  //   console.log("clicked img ... ");
  //
  //   var user_id = $(this).prev().text();
  //
  //   console.log("go to public profile with user id = " + user_id);
  //
  //   window.location.href = baseUrl + "hobbyist/u/" + user_id;
  //
  // });


});

'use strict';

var app = angular.module('myApp', []);

// 修改tag
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.controller('myCtrl', function($rootScope, $scope, $http) {

  var getHListUrl = "/exchcard/api/hobbyist/list/page/1/";

  $http({
    method: "GET",
    url: getHListUrl
  }).then(function mySucces(response) {
    var data = JSON.parse(response.data)
    // console.log(data[0]);
    $scope.hobbyists = data;

  }, function myError(response) {
    // console.log(JSON.stringify(response));
  });

  $scope.visitPublic = function (target) {
    // console.log("clicked item-ng-click ... ");
    // console.log(target);
    var holder = $(target).next();
    // console.log("user id is "+holder.text());
    var user_id = holder.text();

    window.location.href = '/hobbyist/u/'+ user_id;
  }

});