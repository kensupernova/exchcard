'use strict';
var profile_id =$('#profile-id-holder').text().trim();

var getTotal = '/exchcard/api/profiles/'+profile_id+'/cards/all/';

// 使用angular-ui-router实现TAB功能
var app = angular.module('myApp', ['ui.router']);

// 修改tag
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

//  配置state
app.config(["$stateProvider", "$urlRouterProvider", function ($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.when("", "/sentArrived").otherwise('/');

  var sentArrivedState = {
    url:'/sentArrived',
    name:'sentArrived',
    template:
    '<table class = "table-cards"  ng-controller="sentArrivedCtrl" > '+
    '<tr>'+
    '<th class="cell-1">post id</th>'+
    '<th class="cell-2">from user</th>'+
    '<th class="cell-3">from address</th>'+
    '<th class="cell-4">sent time</th>'+
    '<th class="cell-5">to user</th>'+
    '<th class="cell-6">to address</th>'+
    '<th class="cell-7">arrived time</th>'+
    '<th class="cell-8">isArrived</th>'+
    '</tr>'+
    '<tr ng-show="sent_arrived == null"><th colspan ="8">空</th></tr>'+
    '<tr ng-repeat="card in sent_arrived">'+
    '<td>{[{card.card_name}]}</td>'+
    '<td>{[{card.fromsender_email}]}</td>'+
    '<td>{[{card.from_address}]}</td>'+
    '<td>{[{card.sent_date}]}</td>'+
    '<td>{[{card.torecipient_email}]}</td>'+
    '<td>{[{card.to_address}]}</td>'+
    '<td>{[{card.arrived_date}]}</td>'+
    '<td>{[{card.has_arrived}]}</td>'+
    '</tr>'+
    '</table>'
  };

  var receiveArrivedState= {
    url:'/receiveArrived',
    name:'receiveArrived',
    template:
    '<table class = "table-cards receive-arrived"  ng-controller="receiveArrivedCtrl">'+
    '<tr>'+
    '<th>post id</th>'+
    '<th>from user</th>'+
    '<th>from address</th>'+
    '<th>sent time</th>'+
    '<th>to user</th>'+
    '<th>to address</th>'+
    '<th>arrived time</th>'+
    '<th>isArrived</th>'+
    '</tr>'+
    '<tr ng-repeat="card in receive_arrived">'+
    '<td>{[{card.card_name}]}</td>'+
    '<td>{[{card.fromsender_email}]}</td>'+
    '<td>{[{card.from_address}]}</td>'+
    '<td>{[{card.sent_date}]}</td>'+
    '<td>{[{card.torecipient_email}]}</td>'+
    '<td>{[{card.to_address}]}</td>'+
    '<td>{[{card.arrived_date}]}</td>'+
    '<td>{[{card.has_arrived}]}</td>'+
    '</tr>'+
    '<tr ng-show="receive_arrived == null"><th colspan ="8">空</th></tr>'+
    '</table>'
  };

  var sentTravellingState= {
    url:'/sentTravelling',
    name:'sentTravelling',
    template:
    '<table class="table-cards" ng-controller="sentTravellingCtrl" >'+
    '<tr>'+
    '<th>post id</th>'+
    '<th>from user</th>'+
    '<th>from address</th>'+
    '<th>sent time</th>'+
    '<th>to user</th>'+
    '<th>to address</th>'+
    '<th>arrived time</th>'+
    '<th>isArrived</th>'+
    '</tr>'+
    '<tr ng-repeat="card in sent_travelling">'+
    '<td>{[{card.card_name}]}</td>'+
    '<td>{[{card.fromsender_email}]}</td>'+
    '<td>{[{card.from_address}]}</td>'+
    '<td>{[{card.sent_date}]}</td>'+
    '<td>{[{card.torecipient_email}]}</td>'+
    '<td>{[{card.to_address}]}</td>'+
    '<td>{[{card.arrived_date}]}</td>'+
    '<td>{[{card.has_arrived}]}</td>'+
    '</tr>'+
    '<tr ng-show="sent_travelling == null"><th colspan ="8">空</th></tr>'+
    '</table>'
  };

  var receiveTravellingState= {
    url:'/receiveTravelling',
    name:'receiveTravelling',
    template:
    '<table class="table-cards" ng-controller="receiveTravellingCtrl">'+
    '<tr>'+
    '<th>post id</th>'+
    '<th>from user</th>'+
    '<th>from address</th>'+
    '<th>sent time</th>'+
    '<th>to user</th>'+
    '<th>to address</th>'+
    '<th>arrived time</th>'+
    '<th>isArrived</th>'+
    '</tr>'+
    '<tr ng-repeat="card in receive_travelling">'+
    '<td>{[{card.card_name}]}</td>'+
    '<td>{[{card.fromsender_email}]}</td>'+
    '<td>{[{card.from_address}]}</td>'+
    '<td>{[{card.sent_date}]}</td>'+
    '<td>{[{card.torecipient_email}]}</td>'+
    '<td>{[{card.to_address}]}</td>'+
    '<td>{[{card.arrived_date}]}</td>'+
    '<td>{[{card.has_arrived}]}</td>'+
    '</tr>'+
    '<tr ng-show="receive_travelling == null"><th colspan ="8">空</th></tr>'+
    '</table>'
  };

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

    console.log("sucessfully get total cards data!")
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



