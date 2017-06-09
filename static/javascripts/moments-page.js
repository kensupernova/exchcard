(function(){
  // USE JQUERY
  // 我关注用户的活动
  var getActivitiesOfFollowingUrl ="/exchcard/api/moments/followings/activities/";

  var getActivitiesOfFollowingRange ="/exchcard/api/moments/followings/activities/?start=0&end=25";

  addCSRFTokenBeforeAjax();

  $.ajax({
    url: getActivitiesOfFollowingUrl,
    method: "GET",
    success: function (response) {
      // console.log(JSON.stringify(response));
      // console.log(JSON.stringify(response[0]));
      // console.log(JSON.stringify(response[1]));

      response.forEach(function (item, index) {
        $("#moments-container").append(createActItemContent(item));
      })


    },
    error: function (response) {
      // console.log(JSON.stringify(response));
    }

  });

  function createActItemContent(item) {

    var act_short_name = '';

    if(item['activity_type_id'] == 1){
      act_short_name = "发送了一张明信片";// SP
    } else if(item['activity_type_id'] == 2){
      act_short_name = "发送了一张明信片";// SPP
    } else if(item['activity_type_id'] == 3){
      act_short_name = "注册了一张明信片"; // RP
    }  else if(item['activity_type_id'] == 4){
      act_short_name = "注册了一张明信片";// RPP
    } else if(item['activity_type_id'] == 5){
      act_short_name = "上传了一张图片";// UPP
    }

    // IN JSON
    // "created":"2017-05-26T02:59:47.377354Z"
    // var d = new Date('2017-05-26T02:59:47.377354Z')
    // => Fri May 26 2017 10:59:47 GMT+0800 (CST)

    var created = new Date(item['created']); // 已经转化成当地时间, UTC -> UTC+8:00
    var offset = - created.getTimezoneOffset()/60;
    var locale_timezone =  ' GMT+' + offset;

    if (item['has_photo'] || item['has_photo'] == 'true'){
      var text =
        '<div class="act-item-container">' +
        ' <div class="left act-subject-avatar-container">' +
        '   <img src="'+ item["avatar_url"]+'">' +
        ' </div>' +
        '<div class="right act-content-container">' +
        '  <div class="act-text-container">' +
        '    <div class="act-subject">' + item["subject_username"]+'</div>' +
        '    <div class="act-short-name">'+ act_short_name +'</div>' +
        '  </div>' +
        '  <div class="act-photos-container">' +
        '     <img src="'+ item['card_photo_url'] +'">' +
        '  </div>' +
        '  <div class="act-time-container">' + created.toLocaleString() + locale_timezone +'</div>' +
        '</div>' +
        '<br style="display: none; clear: both"/>' +
        '</div>';

    } else{
      var text =
        '<div class="act-item-container">' +
        '  <div class="left act-subject-avatar-container">' +
        '    <img src="'+ item["avatar_url"]+'">' +
        '  </div>' +
        '  <div class="right act-content-container">' +
        '    <div class="act-text-container">' +
        '      <div class="act-subject">' + item["subject_username"]+'</div>' +
        '      <div class="act-short-name">'+ act_short_name +'</div>' +
        '    </div>' +
        '    <div class="act-photos-container">' +
        '    </div>' +
        '    <div class="act-time-container">' + created.toLocaleString() + locale_timezone +'</div>' +
        '  </div>' +
        '  <br style="display: none; clear: both"/>' +
        '</div>';
    }

    return text;

  }


})();
