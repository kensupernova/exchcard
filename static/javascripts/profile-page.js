$(document).ready(function(){
	console.log("profile page ...");
	$(".btn-send-card").click(function () {
    window.location.href="http://localhost:8000/card/send/";
  });

  $(".btn-register-card").click(function () {
    window.location.href="http://localhost:8000/card/register/";
  });

  $("#cards").addClass('active');

});

'use strict';
var profile_id =$('#profile-id-holder').text().trim();
var path = "/exchcard/api/"+"profiles/"+profile_id+"/cards/count";

var app = angular.module('myApp',[]);
//修改tag
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

    $scope.sent_cards_arrived = response.data["sent_cards"]["arrived"];
    $scope.sent_cards_travelling = response.data["sent_cards"]["travelling"];

    $scope.receive_cards_arrived = response.data["receive_cards"]["arrived"];

    $scope.receive_cards_travelling = response.data["receive_cards"]["travelling"];

  }, function myError(response) {

  });

});
