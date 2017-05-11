$(document).ready(function(){
	console.log("profile page ...");

  $(".btn-send-card").click(function () {
    window.location.href="/card/send/";
  });

  $(".btn-receive-card").click(function () {
    window.location.href="/card/receive/";
  });

  $("#cards").addClass('active');

});


'use strict';
var profile_id =$('#profile-id-holder').text().trim();
var BASE_URL = "";
var path = BASE_URL + "/exchcard/api/"+"profiles/"+profile_id+"/cards/allstate/count/";

var app = angular.module('myApp',[]);
// 修改全段angular中的符号, 不与后端python的数据填入符号{{}}混淆
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.controller("myCtrl", function($scope, $http) {

  $http({
  method: "get",
  url: path
  }).then(function mySucces(response) {
    // console.log(JSON.stringify(response.data));

    $scope.sent_cards_arrived = response.data["sent_cards_count"]["arrived"];
    $scope.sent_cards_travelling = response.data["sent_cards_count"]["travelling"];

    $scope.receive_cards_arrived = response.data["receive_cards_count"]["arrived"];
    $scope.receive_cards_travelling = response.data["receive_cards_count"]["travelling"];

  }, function myError(response) {

  });

});
