(function(){
  // USE JQUERY
  // 我关注用户的活动
  var logged_user_id = $("#logged-user-id-holder").text();

  var getActivitiesOfFollowingUrl ="/exchcard/api/moments/followings/activities/";

  var getActivitiesOfFollowingRange ="/exchcard/api/moments/followings/activities/?start=0&end=25";

  addCSRFTokenBeforeAjax();

  $.ajax({
    url: getActivitiesOfFollowingUrl,
    method: "GET",
    success: function (response) {
      // console.log(JSON.stringify(response));
      console.log(JSON.stringify(response[0]));
      console.log(JSON.stringify(response[1]));
      console.log(JSON.stringify("Total actions of my followings " +response.length));


      response.forEach(function (item) {
        $("#moments-container").append(createActItemContent(item));
      });

      // var btns = $(".btn-dianzan");

      // 当用户点击点赞
      $(".btn-dianzan").click(function (event) {
        var btn_dianzan_clicked = $(this);

        // console.log(ele_clicked.html());
        //
        var act_info_container = btn_dianzan_clicked.next();
        // console.log(act_info_container.text());

        var action_id = act_info_container.find(".action-id-holder").text();
        var activity_type_id = act_info_container.find(".activity-type-id-holder").text();
        var activity_short_name = act_info_container.find(".activity-short-name-holder").text();

        // 这些数据不能为空
        if(action_id == "" ||!action_id ||
          action_id == null || action_id == undefined){
          return;
        }

        if(activity_type_id == "" ||!activity_type_id ||
          activity_type_id == null || activity_type_id == undefined){
          return;
        }

        if(activity_type_id == "" ||!activity_type_id ||
          activity_type_id == null || activity_type_id == undefined){
          return;
        }


        //------------------------------------------
        // 发送ajax post 请求

        var makeDianzanUrl = "/exchcard/api/moments/activity/dianzan/toggle/";
        addCSRFTokenBeforeAjax();

        var request_data = {
          action_id: action_id,
          activity_type_id: activity_type_id,
          activity_short_name: activity_short_name
        };

        // console.log("request data: " + JSON.stringify(request_data));

        $.ajax({
          method: "POST",
          url: makeDianzanUrl,
          data: request_data,
          success: function (response) {
            console.log(JSON.stringify(response));
            // console.log("toggle dianzan");

            var zans_container = btn_dianzan_clicked.next().next().next();
            console.log(zans_container.html());
            var div_dianzan_username_str = zans_container.find(".dianzan-username-str");

            // 如果是活跃的, 点赞
            if (response.hasOwnProperty('is_active')){
              if(response['is_active']){
                btn_dianzan_clicked.addClass("btn-feedback-pressed");
                var user_who_zan_username = response["user_who_zan_username"];
                var orgin_text = div_dianzan_username_str.text();

                var names = orgin_text.split(",");

                // console.log("names: " + names.length +': ' +names);
                for(var i = 0; i < names.length; i++){
                  if(names[i] == ''||  names[i]==" "){
                    names.splice(i, 1);
                    break;
                  }
                }

                names.push(user_who_zan_username);

                console.log("names: " + names.length +': ' +names);
                var new_text = names.join(",");
                div_dianzan_username_str.text(new_text);
                console.log("toggle: " + orgin_text +"->" + new_text);

              } else{
                btn_dianzan_clicked.removeClass("btn-feedback-pressed");
                var user_who_zan_username = response["user_who_zan_username"];
                var orgin_text = div_dianzan_username_str.text();

                var dummy_text = orgin_text.replace(user_who_zan_username, '');

                var dummy_names = dummy_text.split(",");

                for(var i=0; i < dummy_names.length; i++){
                  if(dummy_names[i] == ''||  dummy_names[i]==" "){
                    dummy_names.splice(i, 1);
                    break;
                  }
                }

                var new_text = dummy_names.join(",");
                div_dianzan_username_str.text(new_text);
                // console.log("toggle: " + orgin_text +"->" + new_text);

              }
            }

          },
          error: function (response) {
            console.log(JSON.stringify(response));
            // alert(JSON.stringify(response));
            console.log("Fail to make dianzan!");
          }
        });

      });


    },
    error: function (response) {
      // console.log(JSON.stringify(response));
      // console.log("Fail to download activities");
      // alert("Fail to download activities. Server Error!");

      $("#moments-container").append("<div style='color:red; margin-top: 20px;'>" +
        '下载关注用户最新动态失败!' +"</div>");
    }

  });

  function createActItemContent(item) {

    var act_describe_zh = '';

    if(item['activity_type_id'] == 1){
      act_describe_zh = "发送了一张明信片";// SP
    } else if(item['activity_type_id'] == 2){
      act_describe_zh = "发送了一张明信片";// SPP
    } else if(item['activity_type_id'] == 3){
      act_describe_zh = "注册了一张明信片"; // RP
    }  else if(item['activity_type_id'] == 4){
      act_describe_zh = "注册了一张明信片";// RPP
    } else if(item['activity_type_id'] == 5){
      act_describe_zh = "上传了一张图片";// UPP
    }

    // IN JSON
    // "created":"2017-05-26T02:59:47.377354Z"
    // var d = new Date('2017-05-26T02:59:47.377354Z')
    // => Fri May 26 2017 10:59:47 GMT+0800 (CST)

    var created = new Date(item['created']); // 已经转化成当地时间, UTC -> UTC+8:00
    var offset = - created.getTimezoneOffset()/60;
    var locale_timezone =  ' GMT+' + offset;


    // --------------------------
    // feedbacks
    var count = 0; // 点赞总数
    var dianzans_username_str = ''; // 点赞用户名字串
    var hasIDianzanThisAction = false;

    if(item.hasOwnProperty('feedback')){
      var feedback = item['feedback'];
      if(feedback.hasOwnProperty('dianzans')){
        var dianzans = feedback['dianzans'];
        count = dianzans.length;
        dianzans.forEach(function (item) {
          if(item['user_who_zan_id'] == logged_user_id ){
            console.log("你已经给这个活动点赞了! " + logged_user_id +", " + item['user_who_zan_id']);
            hasIDianzanThisAction = true;
          }
          dianzans_username_str += item['user_who_zan_username'] +","
        });

        dianzans_username_str = dianzans_username_str.slice(0, -1);

      }

    }

    var div_btn_dianzan = '';
    if(hasIDianzanThisAction){
      div_btn_dianzan = '  <div class="btn-feedback btn-feedback-pressed btn-dianzan"   >';
    } else{
      div_btn_dianzan = '  <div class="btn-feedback btn-dianzan"   >';
    }

    var div_photo_str = '';

    if (item['has_photo'] || item['has_photo'] == 'true'){
      div_photo_str =
        '  <div class="act-photos-container">' +
        '    <img src="'+ item['card_photo_url'] +'">' +
        '  </div>';

    } else{
      div_photo_str=
        '    <div class="act-photos-container">' +
        '    </div>';
    }


    var text=
      '<div class="act-item-container">' +
      ' <div class="left act-subject-avatar-container">' +
      '   <img src="'+ item["avatar_url"]+'">' +
      ' </div>' +
      '<div class="right act-content-container">' +
      '  <div class="act-text-container">' +
      '    <div class="act-subject">' + item["subject_username"]+'</div>' +
      '    <div class="act-short-name">'+ act_describe_zh +'</div>' +
      '  </div>' +
      div_photo_str +
      '  <div class="act-time-container">' + created.toLocaleString() + locale_timezone +'</div>' +
      '  <div class="btn-feedback-container"> ' +
      div_btn_dianzan +
      '    <img class="img-icon" src="/static/images/thumbs2.png"/><span>点赞</span>' +
      '   </div>' +
      '  <div class="act-info-holder" style="display: none;">' +
      '    <div class="action-id-holder" style="display: none;">' + item['action_id'] +'</div>' +
      '    <div class="user-who-action-id-holder" style="display: none;">' + item['user_id_who_made_actions'] +'</div>' +
      '    <div class="activity-type-id-holder" style="display: none;">' + item['activity_type_id']+ '</div>' +
      '    <div class="activity-short-name-holder" style="display: none;">' +  item['activity_short_name'] +'</div>' +
      '  </div>' +
      '  <div class="btn-feedback btn-comment">' +
      '    <img class="img-icon" src="/static/images/comment1.png"/><span>评论</span>' +
      '  </div>' +
      '  <div class="dianzans-container">' +
      '    <img class="dianzan-img img-icon" src="/static/images/thumbs2.png"/>' +
      '    <div class="dianzan-username-str">' + dianzans_username_str +'</div>' +
      ' </div>' +
      ' <div class="comment-container"></div>' +
      '</div>' +
      '<br style="display: none; clear: both"/>' +
      '</div>';

    return text;

  }

})();
