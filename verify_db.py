#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from commodity.models import CommodityInfos

print("数据库商品列表：")
print("=" * 80)

products = CommodityInfos.objects.all()
print(f"共找到 {products.count()} 件商品")
print("-" * 80)

for i, product in enumerate(products, 1):
    print(f"{i:2d}. {product.name}")
    print(f"    价格: ¥{product.price}, 折扣: ¥{product.discount}")
    print(f"    类型: {product.types}, 销量: {product.sold}")
    print(f"    图片: {product.img}")
    print()

print("=" * 80)
print("数据库连接成功！")
