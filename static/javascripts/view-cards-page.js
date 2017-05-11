console.log("view cards ... ")
'use strict';
var profile_id =$('#profile-id-holder').text().trim();

var getTotal = '/exchcard/api/profiles/'+profile_id+'/cards/total/';

// 使用angular-ui-router实现TAB功能
var app = angular.module('myApp', ['ui.router']);

// 修改tag
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});


app.config(["$stateProvider", "$urlRouterProvider", function ($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.when("", "/sentArrived").otherwise('/');

  var sentArrivedState = {
    url:'/sentArrived',
    name:'sentArrived',
    template:
    '<table class = ""  ng-controller="sentArrivedCtrl">'+
    '<tr>'+
    '<th>post id</th>'+
    '<th>sent time</th>'+
    '<th>from user</th>'+
    '<th>from address</th>'+
    '<th>to user</th>'+
    '<th>to address</th>'+
    '<th>arrived time</th>'+
    '<th>arrived or not</th>'+
    '</tr>'+
    '<tr ng-repeat="card in sent_arrived">'+
    '<td>{[{card.card_name}]}</td>'+
    '<td>{[{card.sent_date}]}</td>'+
    '<td>{[{card.fromsender_email}]}</td>'+
    '<td>{[{card.from_address}]}</td>'+
    '<td>{[{card.torecipient_email}]}</td>'+
    '<td>{[{card.to_address}]}</td>'+
    '<td>{[{card.arrived_date}]}</td>'+
    '<td>{[{card.has_arrived}]}</td>'+
    '</tr>'+
    '</table>'
  }

  var receiveArrivedState= {
    url:'/receiveArrived',
    name:'receiveArrived',
        template:
        '<table class = "receive-arrived"  ng-controller="receiveArrivedCtrl">'+
        '<tr>'+
        '<th>post id</th>'+
        '<th>sent time</th>'+
        '<th>from user</th>'+
        '<th>from address</th>'+
        '<th>to user</th>'+
        '<th>to address</th>'+
        '<th>arrived time</th>'+
        '<th>arrived or not</th>'+
        '</tr>'+
        '<tr ng-repeat="card in receive_arrived">'+
        '<td>{[{card.card_name}]}</td>'+
        '<td>{[{card.sent_date}]}</td>'+
        '<td>{[{card.fromsender_email}]}</td>'+
        '<td>{[{card.from_address}]}</td>'+
        '<td>{[{card.torecipient_email}]}</td>'+
        '<td>{[{card.to_address}]}</td>'+
        '<td>{[{card.arrived_date}]}</td>'+
        '<td>{[{card.has_arrived}]}</td>'+
        '</tr>'+
        '</table>'
  }

  var sentTravellingState= {
    url:'/sentTravelling',
    name:'sentTravelling',
    template:
    '<table  ng-controller="sentTravellingCtrl">'+
    '<tr>'+
    '<th>post id</th>'+
    '<th>sent time</th>'+
    '<th>from user</th>'+
    '<th>from address</th>'+
    '<th>to user</th>'+
    '<th>to address</th>'+
    '<th>arrived time</th>'+
    '<th>arrived or not</th>'+
    '</tr>'+
    '<tr ng-repeat="card in sent_travelling">'+
    '<td>{[{card.card_name}]}</td>'+
    '<td>{[{card.sent_date}]}</td>'+
    '<td>{[{card.fromsender_email}]}</td>'+
    '<td>{[{card.from_address}]}</td>'+
    '<td>{[{card.torecipient_email}]}</td>'+
    '<td>{[{card.to_address}]}</td>'+
    '<td>{[{card.arrived_date}]}</td>'+
    '<td>{[{card.has_arrived}]}</td>'+
    '</tr>'+
    '</table>'
  }

  var receiveTravellingState= {
    url:'/receiveTravelling',
    name:'receiveTravelling',
    template:
    '<table  ng-controller="receiveTravellingCtrl">'+
    '<tr>'+
    '<th>post id</th>'+
    '<th>sent time</th>'+
    '<th>from user</th>'+
    '<th>from address</th>'+
    '<th>to user</th>'+
    '<th>to address</th>'+
    '<th>arrived time</th>'+
    '<th>arrived or not</th>'+
    '</tr>'+
    '<tr ng-repeat="card in receive_travelling">'+
    '<td>{[{card.card_name}]}</td>'+
    '<td>{[{card.sent_date}]}</td>'+
    '<td>{[{card.fromsender_email}]}</td>'+
    '<td>{[{card.from_address}]}</td>'+
    '<td>{[{card.torecipient_email}]}</td>'+
    '<td>{[{card.to_address}]}</td>'+
    '<td>{[{card.arrived_date}]}</td>'+
    '<td>{[{card.has_arrived}]}</td>'+
    '</tr>'+
    '</table>'
  }

  // 注册各个状态
  $stateProvider
    .state(sentArrivedState)
    .state(receiveArrivedState)
    .state(sentTravellingState)
    .state(receiveTravellingState);


}]);

///// 运行app
app.run(function($rootScope, $http) {
  var csrftoken = Cookies.get('csrftoken');

  $http({
    method: "GET",
    headers: {
      'X-CSRFToken': csrftoken
    },
    url: getTotal
  }).then(function mySucces(response) {

    $rootScope.sent_arrived = response.data['sent_arrived'];
    $rootScope.receive_arrived = response.data['receive_arrived'];

    $rootScope.sent_travelling = response.data['sent_travelling'];
    $rootScope.receive_travelling = response.data['receive_travelling'];

    console.log("sucessfully get cards data total!")
    // console.log(JSON.stringify(response.data['sent_arrived'].length));
    // console.log(JSON.stringify(response.data['receive_arrived'].length));
    // console.log(JSON.stringify(response.data['sent_travelling'].length));
    // console.log(JSON.stringify(response.data['receive_travelling'].length));

    // 点击第一个tab, 相当于点击shref
    // $('#tab-sent-arrived').click();

    // TODO: Refresh the ui-view

  }, function myError(response) {
    // console.log("fail to get cards data!");
  });
});


app.controller('sentArrivedCtrl',  function($scope, $rootScope) {
  $scope.sent_arrived = $rootScope.sent_arrived;

  // console.log("rendering sent arrived");
});

app.controller('receiveArrivedCtrl', function($scope, $rootScope) {
  $scope.receive_arrived = $rootScope.receive_arrived;

  // console.log("rendering receive arrived");
});

app.controller('sentTravellingCtrl', function($scope, $rootScope) {
  $scope.sent_travelling = $rootScope.sent_travelling;

  // console.log("rendering sent travelling");
});

app.controller('receiveTravellingCtrl', function($scope, $rootScope) {
  $scope.receive_travelling = $rootScope.receive_travelling;

  // console.log("rendering receive travelling");
});



$(document).ready(function(){

  $("#cards").addClass('active');

});



