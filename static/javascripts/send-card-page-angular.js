/**
 * Created by Guanghui on 2017/6/5.
 */
$(document).ready(function(){

  $("#cards").addClass('active');

});

'use strict';

var getAddress = "/exchcard/api/"+'cards/add/';

var app = angular.module('myApp', ['ui.router']);

//修改tag
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});


app.config(["$stateProvider", "$urlRouterProvider", function ($stateProvider, $urlRouterProvider) {

  // Setup router
  $urlRouterProvider.when("", "/warning").otherwise('/');

  var warningState = {
    url: '/warning',
    name: 'warning',
    templateUrl: '/static/templates/exchcard/angular_templates/send-card-warning-page.html'
  };

  var addressState = {
    url: '/address',
    name: 'address',
    templateUrl: '/static/templates/exchcard/angular_templates/send-card-address-success-page.html'
  };

  // 注册各个状态
  $stateProvider
    .state(warningState)
    .state(addressState);

}]);



app.controller('warningCtrl', function($rootScope, $scope, $http) {

  $scope.confirmGetAddress = function() {

    // console.log("here .... ");

    var csrftoken = Cookies.get('csrftoken');

    $http({
      method: "POST",
      headers: {
        'X-CSRFToken': csrftoken
      },
      url: getAddress
    }).then(function mySucces(response) {

      // response = JSON.parse(response);
      // console.log("new card address: "+JSON.stringify(response.data));

      var postcard_id = response.data.card_name;

      if(postcard_id|| postcard_id==null|| postcard_id==undefined ||
        address || address == null){
        $scope.request_address_error = "fail to get an address";
      }

      $rootScope.postal_info = response.data;

      window.location.href = "/card/travelling/"+postcard_id+"/";

      // METHOD 2
      // // 隐藏提示内容,呈现邮寄地址内容
      // // $('#tab-confirm').click(); // 在angular中无效
      // document.getElementById("tab-confirm").click();


    }, function myError(response) {

    });

  };

});

app.controller('addressCtrl', function($rootScope, $scope) {

  // console.log("new card address: "+JSON.stringify($rootScope.postal_info));

  if($rootScope.postal_info && $rootScope.postal_info != null ){
    $scope.postal_info = $rootScope.postal_info;

  } else{
    $scope.postal_info = null;
  }


});