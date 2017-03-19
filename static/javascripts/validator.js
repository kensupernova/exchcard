/**
 * Created by Guanghui on 2016/12/13.
 */

function regexTest(value, regex){
  return regex.test(value);
}

function validate_username(username){
  // console.log("validating... email");
  var value = username;
  if(!value ||value == null ||value == undefined || value.length==0){
    return false;
  }

  var re = /^[\u4e00-\u9fa5.-@a-zA-Z0-9]{2,25}|[.-@a-zA-Z0-9]{2,30}$/

  return re.test(value);
}

function validate_email(email){
  // console.log("validating... email");

  if(!email ||email == null ||email == undefined || email.length==0){
    return false;
  }

  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}


function validate_password(password){
  // console.log("validating... pw");
  var str = password;

  if(!str ||str == null ||str == undefined || str.length==0){
    return false;
  }

  var minNum = 6;
  var maxNum = 16
  // 6-16位, 数字, 大小写字母, 已经特殊字符!@#$%^&*, 至少一个数字, 至少一个字母
  // var regularExpression2 = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$/;
  var regularExpression = /^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9!@#$%^&*]{6,16})$/;
  if(password.length < minNum || password.length > maxNum){
    return false;
  }

  return regularExpression.test(password);

}

// console.log(validate_password("1111111a"));
// console.log(validate_password("1111111a"));
// console.log(validate_password("zgh4@126"));

function validate_name(name) {
  // console.log("validating... ");
  var str = name;

  if(!str ||str == null ||str == undefined || str.length==0){
    return false;
  }


  // 中国名字: 2到10位汉字,可以包括点号, 至少两位汉字
  // 外国名字: 3-30位, 可以包括空格,点号
  var re = /^((?=.{2}[\u4e00-\u9fa5])[\u4e00-\u9fa5 .a-zA-Z]{2,10})|([a-zA-Z. ]{3,30})$/;
  return re.test(name);
}

// console.log(validate_name("zghfafafa"))
// console.log(validate_name("  "));
// console.log(validate_name("aaaaaaa1"));
// console.log(validate_name(".."));
// console.log(validate_name("张."));
// console.log(validate_name("张.张"));
// console.log(validate_name("a.a"));
// console.log(validate_name("a a"));

function validate_address(address) {
  // console.log("validating... add");
  var str = address;

  if(!str ||str == null ||str == undefined || str.length==0){
    return false;
  }

  // 2-50位汉字
  // 5-100位字母
  var re = /^([\u4e00-\u9fa5 a-zA-Z0-9.-]{2,50})|(?=[a-zA-Z]{3})([ a-zA-Z0-9.-]{5,100})$/;
  return re.test(address);
}

// console.log(validate_address("."))
// console.log(validate_address("10000"))

function validate_postcode(postcode) {
  // console.log("validating... add");
  var str = postcode;

  if(!str ||str == null ||str == undefined || str.length==0){
    return false;
  }


  var re = /^[a-zA-Z0-9.-]{3,11}$/;
  var us = /(^\d{5}$)|(^\d{5}-\d{4}$)/;
  return re.test(postcode);
}

function validate_mobile (value){
  var mobileRegex =  /^(((1[3456789][0-9]{1})|(15[0-9]{1}))+\d{8})$/;
  return mobileRegex.test(value);
}

function validate_chineseId(value){
  var regIdNo = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
  return regIdNo.test(value);
}