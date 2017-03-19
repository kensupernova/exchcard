'use strict';
// var profile_id =$('#profile-id-holder').text().trim();
var getAddress = "/exchcard/api/"+'cards/add/';

var app = angular.module('myApp',[]);
//修改tag
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {
  $scope.confirmSendCard = function() {

    var csrftoken = Cookies.get('csrftoken');
    $http({
      method: "POST",
      headers: {
        'X-CSRFToken': csrftoken
      },
      url: getAddress
    }).then(function mySucces(response) {
      // console.log(JSON.stringify(response.data));
      var torecipient = response.data.torecipient;
      var postid = response.data.card_name;
      if(postid|| postid==null|| postid==undefined ||
        address || address == null){
        $scope.request_address_error = "fail to get an address";
      } else{
        // $scope.post_id = postid;
        // $scope.torecipient_name = torecipient['name'];
        // $scope.torecipient_address = torecipient['address'];
        // $scope.torecipient_postcode = torecipient['postcode'];
        // $scope.torecipient = torecipient;


      }

      window.location.href = "/card/travelling/"+postid+"/";

    }, function myError(response) {

    });

  };

}]);