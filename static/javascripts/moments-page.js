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
      data = JSON.parse(response);
      console.log(JSON.stringify(data));

      data.forEach(function (item, index) {
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
      act_short_name = "发送了一张明信片";
    } else if(item['activity_type_id'] == 2){
      act_short_name = "注册了一张明信片";
    }

    var created = new Date(item['created']);
    var created_str = created.getFullYear() +"." +
      (created.getMonth() + 1) +"." +
      created.getDate() +" " +
      created.getHours() +":" +
      created.getMinutes() +
      " UTC";


    var text =
      '<div class="act-item-container">' +
      ' <div class="left act-subject-avatar-container">' +
      '   <img src="'+ item["avatar_url"]+'">' +
      ' </div>' +
      '<div class="right act-content-container">' +
      '  <div class="act-short-container">' +
      '    <div class="act-subject">' + item["subject_username"]+'</div>' +
      '    <div class="act-short-name">'+ act_short_name +'</div>' +
      '     </div>' +
      '     <div class="act-time-container">' + created_str +'</div>' +
      '     <div class="act-photos-container">' +
      '       <img src="">' +
      '       <img src="">' +
      '     </div>' +
      '   </div>' +
      '<br style="display: none; clear: both"/>' +
      '</div>';

    return text;

  }


})();
