母婴商城 - Baby Mall
基于 Django 框架开发的母婴商品电商网站，提供商品展示、购物车、订单管理、用户认证等完整功能。
技术栈
- 框架: Django 4.2
- 语言: Python 3.9+
- 数据库: MySQL / SQLite
- 前端: HTML5, CSS3, JavaScript, Bootstrap
- 图标: Font Awesome
功能特性
已实现功能
1. 商品管理
   - 商品分类展示（奶粉辅食、宝宝用品、童装、儿童玩具等）
   - 商品列表分页展示
   - 商品详情页
   - 商品搜索功能
   - 销量、价格、收藏排序
2. 购物车功能
   - 添加商品到购物车
   - 更新商品数量
   - 删除购物车商品
   - 清空购物车
   - 全选/取消全选
   - 实时计算总价
3. 订单系统
   - 确认订单页面
   - 多种支付方式选择
   - 订单创建与提交
   - 订单状态管理
   - 订单成功页面
4. 收货地址管理
   - 添加收货地址
   - 修改地址
   - 删除地址
   - 设置默认地址
   - 多地址支持
5. 用户认证
   - 用户注册
   - 用户登录
   - 用户退出
   - 个人中心
   - 订单列表查看
6. 首页功能
   - 今日必抢栏目（横向滚动）
   - 商品分类栏目
   - 搜索框

项目结构
mysite/
├── mysite/                    # 项目配置目录
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # 项目配置（数据库、静态文件等）
│   ├── urls.py               # 主URL配置
│   └── wsgi.py
├── commodity/                 # 商品模块
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             # 商品模型（CommodityInfos, Types）
│   ├── urls.py
│   └── views.py              # 商品视图（列表、详情、搜索）
├── index/                    # 首页模块
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py              # 首页视图
├── shopper/                  # 用户模块
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             # 用户、购物车、订单、地址模型
│   ├── urls.py
│   └── views.py              # 用户认证、购物车、订单视图
├── templates/               # 模板目录
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页
│   ├── commodity.html       # 商品列表页
│   ├── detail.html          # 商品详情页
│   ├── shopcart.html        # 购物车页
│   ├── checkout.html        # 结算页
│   ├── order_success.html   # 订单成功页
│   ├── login.html           # 登录/注册页
│   └── profile.html         # 个人中心页
├── media/                   # 媒体文件（商品图片等）
│   └── imgs/
├── static/                  # 静态文件
├── manage.py               # Django管理命令
└── README.md               # 项目说明文档

快速开始
环境要求
- Python 3.9+
- Django 4.2+
- MySQL 5.7+ 或 SQLite（开发环境）
安装步骤
1.克隆项目
git clone <repository-url>
cd mysite

安装依赖
pip install django pymysql

配置数据库
修改 mysite/settings.py 中的数据库配置：
使用 MySQL（生产环境）：
python运行

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'baby-3',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
（数据库需有数据，可通过babys.sql导入）

使用 SQLite（开发环境）：
python运行

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

数据库迁移
运行 python manage.py migrate

启动开发服务器
运行python manage.py runserver 127.0.0.1:8000

访问网站
打开浏览器访问：http://127.0.0.1:8000

页面路由
| 页面       | URL                          | 说明           |
|------------|------------------------------|----------------|
| 首页       | `/`                          | 网站首页       |
| 商品列表   | `/commodity/`                | 所有商品列表   |
| 商品详情   | `/commodity/detail/<id>/`    | 商品详情页     |
| 购物车     | `/shopper/`                  | 购物车页面     |
| 结算       | `/shopper/checkout/`         | 确认订单页面   |
| 订单成功   | `/shopper/order/success/`    | 订单成功页面   |
| 登录/注册  | `/shopper/login/`            | 用户登录注册   |
| 个人中心   | `/shopper/profile/`          | 用户个人中心   |
| 退出       | `/shopper/logout/`           | 用户退出       |

数据库模型
CommodityInfos（商品信息）
| 字段     | 类型        | 说明       |
|----------|-------------|------------|
| id       | Integer     | 主键       |
| name     | CharField   | 商品名称   |
| price    | FloatField  | 商品价格   |
| types    | CharField   | 商品类型   |
| discount | FloatField  | 折扣价格   |
| stock    | IntegerField| 库存数量   |
| sold     | IntegerField| 已售数量   |
| likes    | IntegerField| 收藏数量   |
| img      | FileField   | 商品图片   |

User（用户信息）
| 字段        | 类型        | 说明           |
|-------------|-------------|----------------|
| id          | Integer     | 主键           |
| username    | CharField   | 用户名         |
| password    | CharField   | 密码（加密）   |
| phone       | CharField   | 手机号         |
| avatar      | FileField   | 用户头像       |
| create_time | DateTimeField| 注册时间      |

CartInfos（购物车信息）
| 字段      | 类型        | 说明       |
|-----------|-------------|------------|
| id        | Integer     | 主键       |
| commodity | ForeignKey  | 关联商品   |
| user      | ForeignKey  | 关联用户   |
| quantity  | IntegerField| 数量       |
| created   | DateTimeField| 添加时间  |

 OrderInfos（订单信息）
| 字段      | 类型        | 说明       |
|-----------|-------------|------------|
| id        | Integer     | 主键       |
| order_sn  | CharField   | 订单编号   |
| price     | FloatField  | 订单总价   |
| user      | ForeignKey  | 关联用户   |
| state     | IntegerField| 订单状态   |
| address   | ForeignKey  | 关联地址   |
| created   | DateTimeField| 创建时间  |

AddressInfos（收货地址）
| 字段       | 类型        | 说明         |
|------------|-------------|--------------|
| id         | Integer     | 主键         |
| user       | ForeignKey  | 关联用户     |
| name       | CharField   | 收货人姓名   |
| phone      | CharField   | 联系电话     |
| province   | CharField   | 省份         |
| city       | CharField   | 城市         |
| district   | CharField   | 区县         |
| detail     | CharField   | 详细地址     |
| is_default | BooleanField| 是否默认     |
| created    | DateTimeField| 创建时间    |

配置说明
媒体文件配置
在 `mysite/settings.py` 中配置：
python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

URL配置
在 `mysite/urls.py` 中添加媒体文件路由：
python
from django.conf import settings
from django.conf.urls.static import static
开发说明
添加商品数据
可以通过 Django Admin 后台添加商品数据：
启动开发服务器
访问 http://127.0.0.1:8000/admin/
使用超级用户登录
在 CommodityInfos 中添加商品
自定义配置
修改模板文件可以改变页面样式
修改视图文件可以改变业务逻辑
修改模型文件需要重新迁移数据库
部署建议
生产环境部署
使用 Gunicorn 或 uWSGI 作为 WSGI 服务器
使用 Nginx 作为反向代理
配置 HTTPS
使用 MySQL 数据库
配置静态文件和媒体文件服务
Docker 部署（推荐）
创建 docker-compose.yml 文件，实现一键部署。

本项目为个人学习与工程实践作品，仅用于学习、演示与简历展示，请勿用于商业用途。
本项目为个人学习与工程实践作品，仅用于学习、演示与简历展示，请勿用于商业用途。
本项目为个人学习与工程实践作品，仅用于学习、演示与简历展示，请勿用于商业用途。
项目开发中，功能持续完善中...
