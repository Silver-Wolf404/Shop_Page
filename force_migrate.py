#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

print("正在删除旧表...")
with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS shopper_cartinfos")
    cursor.execute("DROP TABLE IF EXISTS shopper_orderinfos")
    cursor.execute("DELETE FROM django_migrations WHERE app = 'shopper'")
    print("已删除旧表和迁移记录")

print("正在创建新表...")
os.system('python manage.py makemigrations shopper')
os.system('python manage.py migrate shopper')
