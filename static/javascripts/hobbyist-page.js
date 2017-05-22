/**
 * Created by Guanghui on 2017/5/22.
 */
// var baseUrl = window.location.origin ;
var baseUrl = window.location.protocol +"//"+window.location.ho

$(document).ready(function(){

  $("#hobbyist").addClass('active');


});

'use strict';

var app = angular.module('myApp', []);

// 修改tag
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

var getHListUrl = "/exchcard/api/hobbyist/list/page/1/";

app.controller('myCtrl', function($rootScope, $scope, $http) {


  $http({
    method: "GET",
    url: getHListUrl
  }).then(function mySucces(response) {
    var data = JSON.parse(response.data)
    console.log(data[0]);

    $scope.hobbyists = data;

  }, function myError(response) {
    // console.log(JSON.stringify(response));
  })

});