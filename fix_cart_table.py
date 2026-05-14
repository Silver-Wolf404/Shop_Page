#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS shopper_cartinfos")
    print("已删除旧的购物车表")
    
cursor.close()

print("现在重新创建表...")
os.system('python manage.py makemigrations shopper')
os.system('python manage.py migrate shopper')
