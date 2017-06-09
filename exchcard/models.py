#coding: utf-8

#--------------------------------------------------
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class XUserManager(BaseUserManager):
    """
    通过邮箱，密码创建用户
    """
    def create_user(self, email, username, password=None,type=None,**kwargs):
        if not email:
            raise ValueError(u'用户必须要有邮箱')

        user = self.model(
            email=XUserManager.normalize_email(email),
            username=username,
            type=type if type else 0
        )

        user.set_password(password)

        if kwargs:
            if kwargs.get('sex', None): user.sex = kwargs['sex']
            if kwargs.get('is_active', None): user.is_active=kwargs['is_active']
            if kwargs.get('weibo_uid', None): user.uid=kwargs['weibo_uid']
            if kwargs.get('weibo_access_token', None): user.access_token=kwargs['weibo_access_token']
            if kwargs.get('url', None): user.url=kwargs['url']
            if kwargs.get('desc', None): user.desc=kwargs['desc']
            if kwargs.get('avatar', None): user.avatar=kwargs['avatar']

        user.save(using=self._db) ## 必须save()

        return user

    def create_user_with_no_username(self, email, password=None, type=None, **kwargs):
        if not email:
            raise ValueError(u'用户必须要有邮箱')

        # 瞒天过海，把邮箱地址转化为用户名
        username = email.replace("@", "at")
        username = username.replace(".", "dot")

        user = self.model(
            email=XUserManager.normalize_email(email),
            username=username,
            type=type if type else 0,
            **kwargs
        ) ## 必须用obj.save()

        user.set_password(password)
        user.save(using=self._db)

        return user
    #


    def create_superuser(self, email, username, password):
        """
        创建超级用户
        :param email:
        :param username:
        :param password:
        :return:
        """
        user = self.create_user(email,
            password=password,
           username=username,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user



class XUser(AbstractBaseUser):
    """
    Extended User Model, customize user model,
    AbstractBaseUser already has:
    - password,
    - get_username()
    - is_anonymous()
    - is_authenticated()
    - set_password(raw_password)
      - Taking care of the password hashing. Doesn’t save the AbstractBaseUser object, call obj.save() afterwards
    - check_password(raw_password)
      - Returns True if the given raw string is the correct password for the user
    """
    created = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(verbose_name='Email', max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    type = models.IntegerField(default=0)  # 类型，0本站注册，1微博注册登录

    sex = models.IntegerField(default=1)  # sex
    weibo_uid = models.CharField(max_length=50, null=True)  # weibo uid
    weibo_access_token = models.CharField(max_length=100, null=True)  # weibo access_token
    desc = models.CharField(max_length=2000, null=True)  # 个人信息简介

    url = models.URLField(null=True)  # 个人站点
    avatar = models.CharField(max_length=500, null=True)  # 头像

    objects = XUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def get_username(self):
        return self.username


    def __unicode__(self):
        return u'%s, %s, %s, %s' % (self.type, self.email, self.weibo_uid, self.weibo_access_token)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # def is_authenticated(self):
    #     """
    #     If is_anonymous() == false, return true
    #     :return:
    #     """
    #     return not self.is_anonymous()

    class Meta:
        db_table = 'exchcard_xuser'


class XAuth(object):
    """自定义用户验证"""
    def authenticate(self, email=None, password=None):
        try:
            user = XUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except XUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = XUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except XUser.DoesNotExist:
            return None