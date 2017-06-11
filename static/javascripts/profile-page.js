'use strict';
var profile_id =$('#profile-id-holder').text().trim();
var stateCountUrl = "/exchcard/api/"+"profiles/"+profile_id+"/cards/eachstate/count/";

var allCardsUrl = '/exchcard/api/profiles/'+profile_id+'/cards/all/';

var app = angular.module('myApp', ['ui.router']);

// 修改全段angular中的符号, 不与后端python的数据填入符号{{}}混淆
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

// --------------------------------------------------
//// angular ui router configuration

//  配置state
app.config(["$stateProvider", "$urlRouterProvider", function ($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.when("", "/sentArrived").otherwise('/');

  var sentArrivedState = {
    url:'/sentArrived',
    name:'sentArrived',
    templateUrl: '/static/templates/exchcard/angular_templates/cards/sent-arrived.html',
    // 每次单击调用控制器,不缓存
    cache: false
  };

  var receiveArrivedState= {
    url: '/receiveArrived',
    name: 'receiveArrived',
    templateUrl: '/static/templates/exchcard/angular_templates/cards/receive-arrived.html',
    // 每次单击调用控制器,不缓存
    cache: false
  };

  var sentTravellingState= {
    url: '/sentTravelling',
    name: 'sentTravelling',
    templateUrl: '/static/templates/exchcard/angular_templates/cards/sent-travelling.html',
    // 每次单击调用控制器,不缓存
    cache: false
  };

  var receiveTravellingState= {
    url: '/receiveTravelling',
    name: 'receiveTravelling',
    templateUrl: '/static/templates/exchcard/angular_templates/cards/receive-travelling.html',
    // 每次单击调用控制器,不缓存
    cache: false
  };

  // var sentArrivedState = {
  //   url:'/sentArrived',
  //   name:'sentArrived',
  //   template:
  //   '<table class = "table-cards"  ng-controller="sentArrivedCtrl" > '+
  //   '<tr>'+
  //   '<th class="cell-1">post id</th>'+
  //   '<th class="cell-2">from user</th>'+
  //   '<th class="cell-3">from address</th>'+
  //   '<th class="cell-4">sent time</th>'+
  //   '<th class="cell-5">to user</th>'+
  //   '<th class="cell-6">to address</th>'+
  //   '<th class="cell-7">arrived time</th>'+
  //   '<th class="cell-8">isArrived</th>'+
  //   '</tr>'+
  //   '<tr ng-show="sent_arrived == null"><th colspan ="8">空</th></tr>'+
  //   '<tr ng-repeat="card in sent_arrived">'+
  //   '<td>{[{card.card_name}]}</td>'+
  //   '<td>{[{card.fromsender_email}]}</td>'+
  //   '<td>{[{card.from_address}]}</td>'+
  //   '<td>{[{card.sent_date}]}</td>'+
  //   '<td>{[{card.torecipient_email}]}</td>'+
  //   '<td>{[{card.to_address}]}</td>'+
  //   '<td>{[{card.arrived_date}]}</td>'+
  //   '<td>{[{card.has_arrived}]}</td>'+
  //   '</tr>'+
  //   '</table>'
  // };
  //
  // var receiveArrivedState= {
  //   url:'/receiveArrived',
  //   name:'receiveArrived',
  //   template:
  //   '<table class = "table-cards receive-arrived"  ng-controller="receiveArrivedCtrl">'+
  //   '<tr>'+
  //   '<th>post id</th>'+
  //   '<th>from user</th>'+
  //   '<th>from address</th>'+
  //   '<th>sent time</th>'+
  //   '<th>to user</th>'+
  //   '<th>to address</th>'+
  //   '<th>arrived time</th>'+
  //   '<th>isArrived</th>'+
  //   '</tr>'+
  //   '<tr ng-repeat="card in receive_arrived">'+
  //   '<td>{[{card.card_name}]}</td>'+
  //   '<td>{[{card.fromsender_email}]}</td>'+
  //   '<td>{[{card.from_address}]}</td>'+
  //   '<td>{[{card.sent_date}]}</td>'+
  //   '<td>{[{card.torecipient_email}]}</td>'+
  //   '<td>{[{card.to_address}]}</td>'+
  //   '<td>{[{card.arrived_date}]}</td>'+
  //   '<td>{[{card.has_arrived}]}</td>'+
  //   '</tr>'+
  //   '<tr ng-show="receive_arrived == null"><th colspan ="8">空</th></tr>'+
  //   '</table>'
  // };
  //
  // var sentTravellingState= {
  //   url:'/sentTravelling',
  //   name:'sentTravelling',
  //   template:
  //   '<table class="table-cards" ng-controller="sentTravellingCtrl" >'+
  //   '<tr>'+
  //   '<th>post id</th>'+
  //   '<th>from user</th>'+
  //   '<th>from address</th>'+
  //   '<th>sent time</th>'+
  //   '<th>to user</th>'+
  //   '<th>to address</th>'+
  //   '<th>arrived time</th>'+
  //   '<th>isArrived</th>'+
  //   '</tr>'+
  //   '<tr ng-repeat="card in sent_travelling">'+
  //   '<td>{[{card.card_name}]}</td>'+
  //   '<td>{[{card.fromsender_email}]}</td>'+
  //   '<td>{[{card.from_address}]}</td>'+
  //   '<td>{[{card.sent_date}]}</td>'+
  //   '<td>{[{card.torecipient_email}]}</td>'+
  //   '<td>{[{card.to_address}]}</td>'+
  //   '<td>{[{card.arrived_date}]}</td>'+
  //   '<td>{[{card.has_arrived}]}</td>'+
  //   '</tr>'+
  //   '<tr ng-show="sent_travelling == null"><th colspan ="8">空</th></tr>'+
  //   '</table>'
  // };
  //
  // var receiveTravellingState= {
  //   url:'/receiveTravelling',
  //   name:'receiveTravelling',
  //   template:
  //   '<table class="table-cards" ng-controller="receiveTravellingCtrl">'+
  //   '<tr>'+
  //   '<th>post id</th>'+
  //   '<th>from user</th>'+
  //   '<th>from address</th>'+
  //   '<th>sent time</th>'+
  //   '<th>to user</th>'+
  //   '<th>to address</th>'+
  //   '<th>arrived time</th>'+
  //   '<th>isArrived</th>'+
  //   '</tr>'+
  //   '<tr ng-repeat="card in receive_travelling">'+
  //   '<td>{[{card.card_name}]}</td>'+
  //   '<td>{[{card.fromsender_email}]}</td>'+
  //   '<td>{[{card.from_address}]}</td>'+
  //   '<td>{[{card.sent_date}]}</td>'+
  //   '<td>{[{card.torecipient_email}]}</td>'+
  //   '<td>{[{card.to_address}]}</td>'+
  //   '<td>{[{card.arrived_date}]}</td>'+
  //   '<td>{[{card.has_arrived}]}</td>'+
  //   '</tr>'+
  //   '<tr ng-show="receive_travelling == null"><th colspan ="8">空</th></tr>'+
  //   '</table>'
  // };

  // 注册各个状态
  $stateProvider
    .state(sentArrivedState)
    .state(receiveArrivedState)
    .state(sentTravellingState)
    .state(receiveTravellingState);


}]);


app.run(function($rootScope){
  console.log("angular app is running");
});

app.controller('cardsCtrl', function($rootScope, $http, $state) {
  var csrftoken = Cookies.get('csrftoken');
  $http({
    method: "GET",
    headers: {
      'X-CSRFToken': csrftoken
    },
    url: allCardsUrl
  }).then(function mySucces(response) {

    $rootScope.sent_arrived = response.data['sent_arrived'];
    $rootScope.receive_arrived = response.data['receive_arrived'];

    $rootScope.sent_travelling = response.data['sent_travelling'];
    $rootScope.receive_travelling = response.data['receive_travelling'];

    // console.log("sucessfully get total cards data!")
    // console.log(JSON.stringify(response.data['sent_arrived'].length));
    // console.log(JSON.stringify(response.data['receive_arrived'].length));
    // console.log(JSON.stringify(response.data['sent_travelling'].length));
    // console.log(JSON.stringify(response.data['receive_travelling'].length));

    // 下载数据后, Refresh the ui-view

    // METHOD 1:
    // 点击第一个tab, 相当于点击shref, 相当于refresh ui-view
    document.getElementById("tab-receive-arrived").click();

    // METHOD 2:
    // 一种可以通过$state.go的方式跳转路由，同样可以使用这个参数来处理；
    // 另外一种可以直接使用$state.reload，直接调用$state.reload()是加载整个页面，
    // $state.reload('currentState')则是加载当前路由，这些在源码的注释中都有清晰的说明
    // $state.go('sentArrived');

  }, function myError(response) {
    // console.log("fail to get cards data!");
  });

});


app.controller('sentArrivedCtrl',  function($scope, $rootScope, $state) {
  $scope.sent_arrived = $rootScope.sent_arrived;
  // $state.reload();

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


app.controller("infoCtrl", function($scope, $http) {

  $http({
    method: "get",
    url: stateCountUrl
  }).then(function mySucces(response) {
    // console.log(JSON.stringify(response.data));

    $scope.sent_cards_arrived_count = response.data["sent_cards_count"]["arrived"];
    $scope.sent_cards_travelling_count = response.data["sent_cards_count"]["travelling"];

    $scope.receive_cards_arrived_count = response.data["receive_cards_count"]["arrived"];
    $scope.receive_cards_travelling_count = response.data["receive_cards_count"]["travelling"];

  }, function myError(response) {

  });

  var baseUrl = window.location.protocol +"//"+window.location.host;
  var defaultAvatarUrl = "/static/images/default-avatar.jpg";

  // 有关头像图片的URL
  var getAvatarUrl = "/exchcard/api/profiles/avatar/url/";
  // js.cookie可以产生csrftoken
  var csrftoken = Cookies.get('csrftoken');


  // 下载头像图片
  $http({
    method:"GET",
    headers:{
      'X-CSRFToken': csrftoken
    },
    url: getAvatarUrl
  }).then(function mySucces(response) {
    // console.log(JSON.stringify(response));

    $scope.avatar_url = response.data['avatar'];

  }, function myError(response) {
    // console.log(JSON.stringify(response));

  });

});