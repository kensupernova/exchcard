Exchange Postcard
明信片交流网
====
### 简介  

一个明信片交流网站，陌生人之间交换明信片。只要通过本地注册或者微博注册，填好地址，就
会收到远方朋友的明信片，也可以在旅游时领取任务给陌生的朋友寄送好看的明信片。给别人寄
送的明信片越多，收到的明信片也越多。

### 新浪云配置
index.wsgi ： 给新浪云指定WSGI application 
config.yaml ： 配置部署在新浪云上面   

### 本地运营
运营环境python2.7 
后端依赖包: 
    - Django v1.8.3
    - Django-Rest-Framework v3.3.2
    - MySQL-python v1.2.5

### 前端框架
 - jquery  v2.1.0   
 - bootstrap  v3.3.7
 - angular  v1.6.0   
 - angular-ui-router  v0.3.2   


### 账号系统
1. 本地注册
2. 微博注册

### 明信片发送和接受系统
用户已经可以发送并接受明信片。注意明信片发送时，或者接受到时都是要带照片的。

### TODOS
1. 发烧友 
   所有注册用户的简单名片, 点击名片，可以进入看用户的主页。所有人的主页都是公开的。
   主页上可以：  
       1. 给用户发私信，索要明信片，索要地址
       2. 有一个时间轴，记录用户的活动，包括发送一张明信片，接受一张明信片，评论点赞一条信息。

2. 烧友圈
   自己发送或者别人给自己一张明信片，将在这里显示一条信息。两人之间通过一张明信片建立朋友关系。
   这里可以更新朋友的最新动态。
  
### Small tasks unfinished
1. 邮箱找回秘密








