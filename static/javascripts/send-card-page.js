'use strict';

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
      // console.log("new address: "+JSON.stringify(response.data));
      var torecipient = response.data.torecipient;
      var postcard_id = response.data.card_name;

      if(postcard_id|| postcard_id==null|| postcard_id==undefined ||
        address || address == null){
        $scope.request_address_error = "fail to get an address";
      } else{
        $scope.post_id = postcard_id;
        $scope.torecipient_name = torecipient['name'];
        $scope.torecipient_address = torecipient['address'];
        $scope.torecipient_postcode = torecipient['postcode'];

      }

      window.location.href = "/card/travelling/"+postcard_id+"/";

    }, function myError(response) {

    });

  };

}]);