from django.db import models

# Create your models here.


class Types(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    firsts = models.CharField(max_length=100, verbose_name='一级类型')
    seconds = models.CharField(max_length=100, verbose_name='二级类型')
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = '商品类型'
        verbose_name_plural = '商品类型'


class CommodityInfos(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=500, default='', verbose_name='商品名称')
    price = models.FloatField(default=0, verbose_name='商品价格')
    sezes = models.CharField(max_length=100, default='', verbose_name='颜色规格')
    types = models.CharField(max_length=100, default='', verbose_name='商品类型')
    discount = models.FloatField(default=0, verbose_name='折后价格')
    stock = models.IntegerField(default=0, verbose_name='存货数量')
    sold = models.IntegerField(default=0, verbose_name='已售数量')
    likes = models.IntegerField(default=0, verbose_name='收藏数量')
    created = models.DateField(auto_now_add=True, verbose_name='上架日期')
    img = models.FileField(upload_to=r'imgs', blank=True, null=True, verbose_name='商品主图')
    details = models.FileField(upload_to=r'details', blank=True, null=True, verbose_name='商品介绍')
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'
