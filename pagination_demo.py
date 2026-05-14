#!/usr/bin/env python3
"""
Django分页功能演示脚本
"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# 导入分页功能模块
from django.core.paginator import Paginator

print("=" * 60)
print("Django分页功能演示")
print("=" * 60)

# 生成数据列表
objects = [chr(x) for x in range(97, 107)]
print("\n# 生成数据列表")
print(">>> objects = [chr(x) for x in range(97, 107)]")
print(f">>> objects")
print(f"{objects}")

# 将数据列表以每3个元素分为一页
p = Paginator(objects, 3)
print("\n# 将数据列表以每3个元素分为一页")
print(">>> p = Paginator(objects, 3)")

# 输出全部数据，即整个数据列表
print("\n# 输出全部数据，即整个数据列表")
print(">>> p.object_list")
print(f"{p.object_list}")

# 获取数据列表的长度
print("\n# 获取数据列表的长度")
print(">>> p.count")
print(p.count)

# 分页后的总页数
print("\n# 分页后的总页数")
print(">>> p.num_pages")
print(p.num_pages)

# 将页数转换成range循环对象
print("\n# 将页数转换成range循环对象")
print(">>> p.page_range")
print(p.page_range)

# 获取第二页的数据信息
page2 = p.get_page(2)
print("\n# 获取第二页的数据信息")
print(">>> page2 = p.get_page(2)")

# 判断第二页是否存在上一页
print("\n# 判断第二页是否存在上一页")
print(">>> page2.has_previous()")
print(page2.has_previous())

# 如果当前页存在上一页，就输出上一页的页数
print("\n# 如果当前页存在上一页，就输出上一页的页数")
print(">>> page2.previous_page_number()")
print(page2.previous_page_number())

# 判断第二页是否存在下一页
print("\n# 判断第二页是否存在下一页")
print(">>> page2.has_next()")
print(page2.has_next())

# 如果当前页存在下一页，就输出下一页的页数
print("\n# 如果当前页存在下一页，就输出下一页的页数")
print(">>> page2.next_page_number()")
print(page2.next_page_number())

# 判断当前页是否存在上一页或者下一页
print("\n# 判断当前页是否存在上一页或者下一页")
print(">>> page2.has_other_pages()")
print(page2.has_other_pages())

# 输出第二页所对应的数据内容
print("\n# 输出第二页所对应的数据内容")
print(">>> page2.object_list")
print(page2.object_list)

# 输出第二页的第一行数据在整个数据列表的位置
print("\n# 输出第二页的第一行数据在整个数据列表的位置")
print(">>> page2.start_index()")
print(page2.start_index())

# 输出第二页的最后一行数据在整个数据列表的位置
print("\n# 输出第二页的最后一行数据在整个数据列表的位置")
print(">>> page2.end_index()")
print(page2.end_index())

print("\n" + "=" * 60)
print("演示完成！")
print("=" * 60)

if __name__ == '__main__':
    pass
