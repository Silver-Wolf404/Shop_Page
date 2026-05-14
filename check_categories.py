#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from commodity.models import CommodityInfos

print("数据库中所有商品分类：")
print("=" * 60)

categories = CommodityInfos.objects.values_list('types', flat=True).distinct()
for cat in categories:
    count = CommodityInfos.objects.filter(types=cat).count()
    print(f"'{cat}' - {count} 件商品")

print("\n商品分类查询测试：")
print("-" * 60)
print(f"宝宝服饰: {CommodityInfos.objects.filter(types='宝宝服饰').count()} 件")
print(f"奶粉辅食: {CommodityInfos.objects.filter(types='奶粉辅食').count()} 件")
print(f"宝宝用品: {CommodityInfos.objects.filter(types='宝宝用品').count()} 件")
print(f"童装: {CommodityInfos.objects.filter(types='童装').count()} 件")
print(f"纸尿裤: {CommodityInfos.objects.filter(types='纸尿裤').count()} 件")
print(f"进口奶粉: {CommodityInfos.objects.filter(types='进口奶粉').count()} 件")
