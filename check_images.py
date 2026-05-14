#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from commodity.models import CommodityInfos

for p in CommodityInfos.objects.all()[:3]:
    print(f'商品: {p.name}')
    print(f'  img字段值: {p.img}')
    print(f'  img.url: {p.img.url if p.img else None}')
    if p.img:
        file_path = os.path.join(os.path.dirname(__file__), 'media', str(p.img))
        exists = os.path.exists(file_path)
        print(f'  图片文件存在: {exists}')
        print(f'  文件路径: {file_path}')
    print()
