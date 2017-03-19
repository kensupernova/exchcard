$(document).ready(function(){
  $("#moments").addClass('active');

});

var app = angular.module('myApp', []);

//修改tag
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});


app.controller("myCtrl", function($scope, $http) {

});

