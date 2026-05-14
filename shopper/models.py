import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from commodity.models import CommodityInfos


STATE = {
    (0, '待支付'),
    (1, '已支付'),
    (2, '已发货'),
    (3, '已完成'),
}


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    avatar = models.FileField(upload_to='avatars', blank=True, null=True, verbose_name='头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class CartInfos(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    quantity = models.IntegerField(default=1, verbose_name='购物数量')
    commodity = models.ForeignKey(CommodityInfos, on_delete=models.CASCADE, verbose_name='商品')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='用户')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    def __str__(self):
        return f"{self.user.username} - {self.commodity.name}"
    
    @property
    def subtotal(self):
        price = self.commodity.discount if self.commodity.discount else self.commodity.price
        return price * self.quantity
    
    class Meta:
        verbose_name = '购物车信息'
        verbose_name_plural = '购物车信息'


class OrderInfos(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    order_sn = models.CharField(max_length=50, unique=True, verbose_name='订单编号')
    price = models.FloatField(verbose_name='订单总价')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    state = models.IntegerField(choices=STATE, default=0, verbose_name='订单状态')
    address = models.ForeignKey('AddressInfos', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='收货地址')
    
    @property
    def status_text(self):
        state_dict = dict(STATE)
        return state_dict.get(self.state, '未知')
    
    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = '订单信息'


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    order = models.ForeignKey(OrderInfos, on_delete=models.CASCADE, verbose_name='订单')
    commodity = models.ForeignKey(CommodityInfos, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    price = models.FloatField(verbose_name='单价')
    
    @property
    def subtotal(self):
        return self.price * self.quantity
    
    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'


class AddressInfos(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='用户')
    name = models.CharField(max_length=50, verbose_name='收货人姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    province = models.CharField(max_length=50, verbose_name='省份')
    city = models.CharField(max_length=50, verbose_name='城市')
    district = models.CharField(max_length=50, verbose_name='区县')
    detail = models.CharField(max_length=200, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, verbose_name='是否默认地址')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return f"{self.name} - {self.phone} - {self.province}{self.city}{self.district}{self.detail}"
    
    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址'