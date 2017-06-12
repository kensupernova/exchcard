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

  var getHBasicInfo = "/exchcard/api/hobbyist/u/"+user_id + "/basic/info/";
  var getActivitiesAll = "/exchcard/api/hobbyist/u/"+user_id + "/activities/all/";

  //--------------------------------------------
  // 下载头像图片, 文字信息, 与之关系等基本信息
  $.ajax({
    method:"GET",
    url: getHBasicInfo,
    success: function (response) {
      // console.log(JSON.stringify(response));

      var avatar_url= response['avatar_info']['avatar_url'];
      avatar_url = avatar_url.lastIndexOf("http", 0) === 0 ? avatar_url: response['avatar_info']['avatar'];

      $("#h-img").attr('src', avatar_url);

      $("#text-info-email").text(response['user_email']);
      $("#text-info-username").text(response['username']);
      $("#text-info-user-id-inp").val(response['user_id']);
      $("#text-info-user-id-holder").text(response['user_id']);

      var isFollowingHimInt = response['isFollowingHimInt'];
      if(isFollowingHimInt == 1 || isFollowingHimInt == '1'){
        // var ele = $("#btn-follow-him");
        // ele.addClass("btn-inactive");
        // ele.addClass("following");
        // ele.removeClass("btn-active");
        // ele.text("你已经关注他");
        make_follow_him_btn_inactive();
      }


    }
  }).fail(function (response) {
    console.log(JSON.stringify(response));

  });

  //--------------------------------------------
  // 下载用户所有的活动
  $.ajax({
    method:"GET",
    url: getActivitiesAll,
    success: function (response) {
      // console.log(JSON.stringify(response));
      // console.log(JSON.stringify(response[1]));
      // console.log(JSON.stringify(response[2]));

      if(response == null || !response){
        alert("This user has no activities!");
      }

      response.forEach(function(act){
        $("#timeline-content-container").append(createActItem(act));
      });

    }
  }).fail(function (response) {
    // console.log(JSON.stringify(response));

  });

  function createActItem(act){

    // var txt1="<p>Text.</p>";              // 以 HTML 创建新元素
    // var txt2=$("<p></p>").text("Text.");  // 以 jQuery 创建新元素
    // var txt3=document.createElement("p");
    // txt3.innerHTML="Text.";               // 通过 DOM 来创建文本

    var act_short_name = '';

    if(act['activity_type_id'] == 1){
      act_short_name = "发送了一张明信片";// SP
    } else if(act['activity_type_id'] == 2){
      act_short_name = "发送了一张明信片";// SPP
    } else if(act['activity_type_id'] == 3){
      act_short_name = "注册了一张明信片"; // RP
    }  else if(act['activity_type_id'] == 4){
      act_short_name = "注册了一张明信片";// RPP
    } else if(act['activity_type_id'] == 5){
      act_short_name = "上传了一张图片";// UPP
    }
    var created = new Date(act['created']);
    var created_str = created.toLocaleString();
    var offset = - created.getTimezoneOffset()/60;
    var locale_timezone =  ' GMT+' + offset;

    if(act['has_photo']){
      var mainText =
        '<div class="act-item-container">' +
        '  <div class="act-time-container left">'+ created_str + locale_timezone  +'</div>' +
        '  <div class="act-text-container right">' +
        '    <div class="act-short-name">'+ act_short_name +'</div>' +
        '    <div class="act-photos-container">' +
        '      <div>' +
        '        <img src="'+ act['card_photo_url'] +'"/>' +
        '      </div>' +
        '    </div>' +
        '  </div>' +
        '  <br style="clear: both; display: none;" />'+
        '</div>';
    } else{
      var mainText =
        '<div class="act-item-container">' +
        '  <div class="act-time-container left">'+ created_str + locale_timezone  +'</div>' +
        '  <div class="act-text-container right">' +
        '    <div class="act-short-name">'+ act_short_name +'</div>' +
        '    <div class="act-photos-container">' +
        '    </div>' +
        '  </div>' +
        '  <br style="clear: both; display: none;" />'+
        '</div>';
    }


    return mainText;
  }


  // --------------
  // follow him, make a follow
  $("#btn-follow-him.btn-active").click(function(){
    // 如果按钮失效, 就不能点击!
    if($(this).hasClass("btn-inactive")){
      return;
    }
    // ele.removeClass("btn-active");// ele.removeClass("btn-active");
    // alert("You clicked follow button");
    var followHimUrl = "/exchcard/api/users/follow/him/";

    // var id1 =  $("#text-info-user-id-inp").val();
    // var id2 = $("#text-info-user-id-holder").text();

    var user_id_of_the_hobbyist = $("#text-info-user-id-inp").val();

    if(!user_id_of_the_hobbyist || user_id_of_the_hobbyist == ''){
      return;
    }

    var logged_user_id = $("#logged-user-id-holder").text();
    if(Number(logged_user_id) == Number(user_id_of_the_hobbyist)){
      alert("You can not follow yourself!");
      return;
    }

    // VERY IMPORTANT IN AJAX REQUEST, GET OR POST
    addCSRFTokenBeforeAjax();
    $.ajax({
      url: followHimUrl,
      method: 'POST',
      data: {
        'user_being_followed_id': user_id_of_the_hobbyist
      },
      success: function (response) {
        console.log(JSON.stringify(response));
        var isFollowSuccess1 = response['isFollowSuccessBool'];
        var isFollowSuccess2 = response['isFollowSuccessInt'];
        //
        // alert(typeof isFollowSuccess1); // boolean
        // alert(typeof isFollowSuccess2); // number

        // 成功关注此用户
        if(isFollowSuccess1 || isFollowSuccess2 == 1){
          var ele = $("#btn-follow-him");
          // ele.addClass("btn-inactive");
          // ele.addClass("following");
          // ele.removeClass("btn-active");
          // ele.text("你已经关注他");
          make_follow_him_btn_inactive()
        }

        //
        // 如果已经关注了此用户, 此次关注将不成功, 是个错误。
        // METHOD 1: 第一种处理错误方法, 但是服务器没有报错。
        if(! isFollowSuccess1 || isFollowSuccess2 == 0){
          var isAlreadyFollowingHimInt = response['isAlreadyFollowingHimInt'];
          if(isAlreadyFollowingHimInt == 1){
            alert(response["error_msg"]);
          }
        }



      },
      error: function (response) {
        // METHOD 2: 第二种处理错误方法, 服务器报错了。
        // console.log(JSON.stringify(response));
        data = response["responseJSON"];
        // console.log(JSON.stringify(data));
        //
        var isFollowSuccess1 = data['isFollowSuccessBool'];
        var isFollowSuccess2 = data['isFollowSuccessInt'];
        if(! isFollowSuccess1 || isFollowSuccess2 == 0){
          var isAlreadyFollowingHimInt = data['isAlreadyFollowingHimInt'];
          if(isAlreadyFollowingHimInt == 1){
            alert(data["error_msg"]);
          }
        }
      }
    });

  });

  function make_follow_him_btn_inactive() {
    var ele = $("#btn-follow-him");
    ele.addClass("btn-inactive");
    ele.addClass("following");
    ele.removeClass("btn-active");
    ele.text("你已经关注他");
  }

  function make_follow_him_btn_active() {
    var ele = $("#btn-follow-him");
    ele.removeClass("btn-inactive");
    ele.removeClass("following");
    ele.addClass("btn-active");
    ele.text("关注他");
  }



});

////////////--------------------
//---- USE ANGULAR 1
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
