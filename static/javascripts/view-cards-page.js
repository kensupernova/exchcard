$(document).ready(function(){

  $("#cards").addClass('active');

});

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
    templateUrl: '/static/templates/exchcard/angular_templates/cards/sent-arrived.html'
  };

  var receiveArrivedState= {
    url: '/receiveArrived',
    name: 'receiveArrived',
    templateUrl: '/static/templates/exchcard/angular_templates/cards/receive-arrived.html'
  };

  var sentTravellingState= {
    url: '/sentTravelling',
    name: 'sentTravelling',
    templateUrl: '/static/templates/exchcard/angular_templates/cards/sent-travelling.html'
  };

  var receiveTravellingState= {
    url: '/receiveTravelling',
    name: 'receiveTravelling',
    templateUrl: '/static/templates/exchcard/angular_templates/cards/receive-travelling.html'
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
    // 相当于 Refresh the ui-view
    document.getElementById('#tab-sent-arrived').click();



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







