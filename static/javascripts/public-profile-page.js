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
  var defaultAvatarUrl = "/static/images/default-avatar.jpg";

  var getHBasicTextInfo = "/exchcard/api/hobbyist/u/"+user_id + "/basic/info/";
  var getActivitiesAll = "/exchcard/api/hobbyist/u/"+user_id + "/activities/all/";

  // 下载头像图片
  $.ajax({
    method:"GET",
    url: getHBasicTextInfo,
    success: function (response) {
      // console.log(JSON.stringify(response));

      var avatar_url= response['avatar_info']['avatar_url'];
      avatar_url = avatar_url.lastIndexOf("http", 0) === 0 ? avatar_url: response['avatar_info']['avatar'];
      if(Number(avatar_url.lastIndexOf("http", 0)) != Number(0) ){
        avatar_url = baseUrl + defaultAvatarUrl;
      }
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
      console.log(JSON.stringify(response));


      if(response ==null ){
        alert("This user has no activities!");
      }
    }
  }).fail(function (response) {
    console.log(JSON.stringify(response));

  });

});


