/**
 * Created by Guanghui on 2017/5/26.
 */

$(document).ready(function(){

  $("#hobbyist").addClass('active');

  var baseUrl = window.location.protocol +"//"+window.location.host;
  var currentUrl = window.location.href;
  var ar = currentUrl.split("/");
  // console.log(ar);

  var user_id = ar[5];

  // console.log("user id is " + user_id);

  // 有关头像图片的URL
  // var getAvatarUrl = "/exchcard/api/profiles/avatar/url/";

  var getHBasicTextInfo = "/exchcard/api/hobbyist/u/"+user_id + "/basic/info/";
  var getActivitiesAll = "/exchcard/api/hobbyist/u/"+user_id + "/activities/all/";

  // 下载头像图片等基本信息
  $.ajax({
    method:"GET",
    url: getHBasicTextInfo,
    success: function (response) {
      // console.log(JSON.stringify(response));

      var avatar_url= response['avatar_info']['avatar_url'];
      avatar_url = avatar_url.lastIndexOf("http", 0) === 0 ? avatar_url: response['avatar_info']['avatar'];

      $("#h-img").attr('src', avatar_url);

      $("#text-info-email").text(response['user_email']);

    }
  }).fail(function (response) {
    console.log(JSON.stringify(response));

  });

  $.ajax({
    method:"GET",
    url: getActivitiesAll,
    success: function (response) {
      // console.log(JSON.stringify(response));

      if(response ==null ){
        alert("This user has no activities!");
      }

      var receive_card_act = response["receive_card_actions"];
      var sent_card_act = response["sent_card_actions"];

      receive_card_act.forEach(function(item, index){
        item["activity_id"] = 2;
        item["activity_type"] = 2;
        item["activity_short_name"] = "register postcard";

      });

      sent_card_act.forEach(function(item, index){
        item["activity_id"] = 1;
        item["activity_type"] = 1;
        item["activity_short_name"] = "sent postcard";

      });


      var acts = receive_card_act.concat(sent_card_act);

      acts = acts.sort(function (a, b) {
        // 2017-05-28T02:24:27.353531Z
        // new Date('2017-05-28T02:24:27.353531Z')
        at = new Date(a["created"]);
        bt = new Date(b["created"]);

        return bt - at;
      });

      // console.log(JSON.stringify(acts));

      acts.forEach(function(act){
        $("#act-item-container-1").append(createActItem(act));
      });

    }
  }).fail(function (response) {
    console.log(JSON.stringify(response));

  });

  function createActItem(act){

    // var txt1="<p>Text.</p>";              // 以 HTML 创建新元素
    // var txt2=$("<p></p>").text("Text.");  // 以 jQuery 创建新元素
    // var txt3=document.createElement("p");
    // txt3.innerHTML="Text.";               // 通过 DOM 来创建文本

    var act_short_name = '';

    if(act['activity_id'] == 1){
      act_short_name = "发送了一张明信片";
    } else if(act['activity_id'] == 2){
      act_short_name = "注册了一张明信片";
    }

    var created = new Date(act['created']);
    var created_str = created.getFullYear() +"." +
      (created.getMonth() + 1) +"." +
      created.getDate() +" " +
      created.getHours() +":" +
      created.getMinutes();

    var mainText = '<div class="act-item-container">' +
      '<div class="act-short-container">' +
      '<div class="act-subject">'+ act['subject_username'] +'</div>' +
      '<div class="act-short-name">'+ act_short_name +'</div>' +
      '</div>' +
      '<div class="act-time-container">'+ created_str  +'</div>' +
    '</div>';

    return mainText;
  }




});

// 'use strict';
//
// var baseUrl = window.location.protocol +"//"+window.location.host;
// var currentUrl = window.location.href;
// var ar = currentUrl.split("/");
//
// var user_id = ar[5];
//
// var getActivitiesAll = "/exchcard/api/hobbyist/u/"+user_id + "/activities/all/";
//
// //// --------------------------------
// var app = angular.module('myApp', []);
//
// // 修改全段angular中的符号, 不与后端python的数据填入符号{{}}混淆
// app.config(function($interpolateProvider) {
//   $interpolateProvider.startSymbol('{[{');
//   $interpolateProvider.endSymbol('}]}');
// });
//
//
// app.controller("myCtrl", function($scope, $http) {
//
//   // 下载最新活动
//   $http({
//     method: "get",
//     url: getActivitiesAll
//   }).then(function mySucces(response) {
//     // console.log(JSON.stringify(response));
//
//     if(response ==null ){
//       alert("This user has no activities!");
//     }
//
//     var receive_card_act = response["receive_card_actions"];
//     var sent_card_act = response["sent_card_actions"];
//
//     receive_card_act.forEach(function(item, index){
//       item["activity_id"] = 2;
//       item["activity_type"] = 2;
//       item["activity_short_name"] = "register postcard";
//
//     });
//
//     sent_card_act.forEach(function(item, index){
//       item["activity_id"] = 1;
//       item["activity_type"] = 1;
//       item["activity_short_name"] = "sent postcard";
//
//     });
//
//
//     var acts = receive_card_act.concat(sent_card_act);
//
//     acts = acts.sort(function (a, b) {
//       // 2017-05-28T02:24:27.353531Z
//       // new Date('2017-05-28T02:24:27.353531Z')
//       var at = new Date(a["created"]);
//       var bt = new Date(b["created"]);
//
//       return bt - at;
//     });
//     // console.log(JSON.stringify(acts));
//
//     $scope.activities = acts;
//
//     console.log("act: "+JSON.stringify($scope.activities));
//
//
//   }, function myError(response) {
//     console.log(JSON.stringify(response));
//
//   });
//
// });
//
//
// function handle_initial_act_data(response) {
//   // console.log(JSON.stringify(response));
//
//   var receive_card_act = response["receive_card_actions"];
//   var sent_card_act = response["sent_card_actions"];
//
//   receive_card_act.forEach(function(item, index){
//     item["activity_id"] = 2;
//     item["activity_type"] = 2;
//     item["activity_short_name"] = "register postcard";
//
//   });
//
//   sent_card_act.forEach(function(item, index){
//     item["activity_id"] = 1;
//     item["activity_type"] = 1;
//     item["activity_short_name"] = "sent postcard";
//
//   });
//
//
//   var act = receive_card_act.concat(sent_card_act);
//
//   act = act.sort(function (a, b) {
//     // 2017-05-28T02:24:27.353531Z
//     // new Date('2017-05-28T02:24:27.353531Z')
//     var at = new Date(a["created"]);
//     var bt = new Date(b["created"]);
//
//     return bt - at;
//   });
//
//   // console.log("act: "+JSON.stringify(act));
//
//   if(response ==null ){
//     alert("This user has no activities!");
//   }
// }
//
