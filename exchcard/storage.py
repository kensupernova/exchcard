# -*- coding: utf-8 -*-

from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
import sae.storage
import re

class SAEStorage(Storage):
    def __init__(self, domain_name = ''): #可传入一个参数，即Storage的DomainName，若为空则默认为settings.py中的
        if not domain_name:                  #SAE_DEFAULT_STORAGE_DOMAIN_NAME选项
            domain_name = settings.SAE_DEFAULT_STORAGE_DOMAIN_NAME
        self.__bucket = sae.storage.Bucket(domain_name) #创建Bucket对象

    def delete(self, name):  #重写 删除 方法
        self.__bucket.delete_object(name)

    def exists(self, name):  #重写 判断存在 方法
        try:
            self.__bucket.stat_object(name)
            return True
        except sae.storage.Error:
            return False
    def size(self, name):    #重写 文件大小 方法
        try:
            stat = self.__bucket.stat_object(name)
        except sae.storage.Error:
            return -1
        return int(stat['bytes'])

    def url(self, name):   #重写 获得文件URL 方法
        return self.__bucket.generate_url(name)

    def _open(self, name, mode = 'rb'): #重写 打开文件 方法
        try:
            return ContentFile(self.__bucket.get_object_contents(name))
        except:
            return None

    def _save(self, name, content): #重写 保存文件 方法
        self.__bucket.put_object(name, content)
        return name

    def listdir(self, path): #重写 列目录 方法
        r = re.compile('^%s' % path)
        remove_prefix = lambda name: r.sub('', name)
        return [(remove_prefix(attr['name']), None) for attr in self.__bucket.list(path = path)]