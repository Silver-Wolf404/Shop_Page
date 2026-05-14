from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from commodity.models import CommodityInfos
from shopper.models import CartInfos, OrderInfos, OrderItem, AddressInfos, User
import json
import datetime
import random


def get_current_user(request):
    if request.user.is_authenticated:
        return request.user
    return None


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({'success': False, 'message': '用户名和密码不能为空'})
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': '登录成功'})
            else:
                return JsonResponse({'success': False, 'message': '用户名或密码错误'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            phone = data.get('phone', '')
            
            if not username or not password:
                return JsonResponse({'success': False, 'message': '用户名和密码不能为空'})
            
            if len(password) < 6:
                return JsonResponse({'success': False, 'message': '密码至少需要6位'})
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': '用户名已存在'})
            
            user = User.objects.create_user(username=username, password=password, phone=phone)
            user.save()
            
            login(request, user)
            return JsonResponse({'success': True, 'message': '注册成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


def get_cart_items(request):
    user = get_current_user(request)
    user_id = user.id if user else 0
    return CartInfos.objects.filter(user_id=user_id).select_related('commodity')


def get_addresses(request):
    user = get_current_user(request)
    user_id = user.id if user else 0
    return AddressInfos.objects.filter(user_id=user_id).order_by('-is_default', '-created')


def get_orders(request):
    user = get_current_user(request)
    user_id = user.id if user else 0
    return OrderInfos.objects.filter(user_id=user_id).order_by('-created')


class CartView(View):
    def get(self, request):
        cart_items = get_cart_items(request)
        total_price = sum(item.subtotal for item in cart_items)
        total_count = sum(item.quantity for item in cart_items)
        
        return render(request, 'shopcart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'total_count': total_count,
        })


class AddToCartView(View):
    def post(self, request):
        try:
            if not request.body:
                return JsonResponse({'success': False, 'message': '请求体为空'})
            
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return JsonResponse({'success': False, 'message': 'JSON解析失败: ' + str(e)})
            
            commodity_id = data.get('commodity_id')
            quantity = data.get('quantity', 1)
            
            if not commodity_id:
                return JsonResponse({'success': False, 'message': '商品ID不能为空'})
            
            if not isinstance(quantity, int) or quantity <= 0:
                return JsonResponse({'success': False, 'message': '数量必须为正整数'})
            
            try:
                commodity = CommodityInfos.objects.get(id=commodity_id)
            except CommodityInfos.DoesNotExist:
                return JsonResponse({'success': False, 'message': '商品不存在'})
            
            user = get_current_user(request)
            user_id = user.id if user else 0
            
            cart_item, created = CartInfos.objects.get_or_create(
                commodity=commodity,
                user_id=user_id,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            cart_count = CartInfos.objects.filter(user_id=user_id).count()
            
            return JsonResponse({
                'success': True,
                'message': '已添加到购物车',
                'cart_count': cart_count
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class UpdateCartQuantityView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            cart_id = data.get('cart_id')
            quantity = data.get('quantity')
            
            user = get_current_user(request)
            user_id = user.id if user else 0
            
            cart_item = get_object_or_404(CartInfos, id=cart_id, user_id=user_id)
            
            if quantity <= 0:
                cart_item.delete()
                return JsonResponse({'success': True, 'deleted': True})
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({
                'success': True,
                'subtotal': cart_item.subtotal,
                'total_price': sum(item.subtotal for item in get_cart_items(request))
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class DeleteCartItemView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            cart_id = data.get('cart_id')
            
            user = get_current_user(request)
            user_id = user.id if user else 0
            
            cart_item = get_object_or_404(CartInfos, id=cart_id, user_id=user_id)
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'message': '已删除',
                'total_price': sum(item.subtotal for item in get_cart_items(request))
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class ClearCartView(View):
    def post(self, request):
        try:
            user = get_current_user(request)
            user_id = user.id if user else 0
            CartInfos.objects.filter(user_id=user_id).delete()
            return JsonResponse({'success': True, 'message': '购物车已清空'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class CheckoutView(View):
    def get(self, request):
        cart_items = get_cart_items(request)
        
        if not cart_items:
            return redirect('/shopper/')
        
        total_price = sum(item.subtotal for item in cart_items)
        total_count = sum(item.quantity for item in cart_items)
        
        shipping_fee = 0 if total_price >= 99 else 10
        discount = 0
        final_price = total_price + shipping_fee - discount
        
        addresses = get_addresses(request)
        
        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'total_count': total_count,
            'shipping_fee': shipping_fee,
            'discount': discount,
            'final_price': final_price,
            'addresses': addresses,
        })


class CreateOrderView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            payment_method = data.get('payment_method', 'alipay')
            
            cart_items = get_cart_items(request)
            
            if not cart_items:
                return JsonResponse({'success': False, 'message': '购物车为空'})
            
            user = get_current_user(request)
            user_id = user.id if user else 0
            
            total_price = sum(item.subtotal for item in cart_items)
            shipping_fee = 0 if total_price >= 99 else 10
            discount = 0
            final_price = total_price + shipping_fee - discount
            
            order_sn = 'ORD' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))
            
            order = OrderInfos.objects.create(
                order_sn=order_sn,
                price=final_price,
                user_id=user_id,
                state=1
            )
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    commodity=item.commodity,
                    quantity=item.quantity,
                    price=item.commodity.discount if item.commodity.discount else item.commodity.price
                )
            
            CartInfos.objects.filter(user_id=user_id).delete()
            
            payment_method_display = {
                'alipay': '支付宝',
                'wechat': '微信支付',
                'card': '银行卡'
            }
            
            request.session['order_info'] = {
                'order_sn': order_sn,
                'order_amount': final_price,
                'payment_method': payment_method_display.get(payment_method, '未知'),
                'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return JsonResponse({'success': True, 'message': '订单创建成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class OrderSuccessView(View):
    def get(self, request):
        order_info = request.session.get('order_info')
        
        if not order_info:
            return redirect('/shopper/')
        
        return render(request, 'order_success.html', order_info)


class AddAddressView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            phone = data.get('phone')
            province = data.get('province')
            city = data.get('city')
            district = data.get('district')
            detail = data.get('detail')
            is_default = data.get('is_default', False)
            
            if not name or not phone or not province or not city or not district or not detail:
                return JsonResponse({'success': False, 'message': '请填写完整地址信息'})
            
            user = get_current_user(request)
            user_id = user.id if user else 0
            
            if is_default:
                AddressInfos.objects.filter(user_id=user_id, is_default=True).update(is_default=False)
            
            address = AddressInfos.objects.create(
                user_id=user_id,
                name=name,
                phone=phone,
                province=province,
                city=city,
                district=district,
                detail=detail,
                is_default=is_default
            )
            
            return JsonResponse({
                'success': True,
                'message': '地址添加成功',
                'address': {
                    'id': address.id,
                    'name': address.name,
                    'phone': address.phone,
                    'province': address.province,
                    'city': address.city,
                    'district': address.district,
                    'detail': address.detail,
                    'is_default': address.is_default
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class DeleteAddressView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            address_id = data.get('address_id')
            
            user = get_current_user(request)
            user_id = user.id if user else 0
            
            address = get_object_or_404(AddressInfos, id=address_id, user_id=user_id)
            address.delete()
            
            return JsonResponse({'success': True, 'message': '地址已删除'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class SetDefaultAddressView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            address_id = data.get('address_id')
            
            user = get_current_user(request)
            user_id = user.id if user else 0
            
            AddressInfos.objects.filter(user_id=user_id, is_default=True).update(is_default=False)
            
            address = get_object_or_404(AddressInfos, id=address_id, user_id=user_id)
            address.is_default = True
            address.save()
            
            return JsonResponse({'success': True, 'message': '已设为默认地址'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class GetAddressesView(View):
    def get(self, request):
        try:
            user = get_current_user(request)
            user_id = user.id if user else 0
            
            addresses = AddressInfos.objects.filter(user_id=user_id).order_by('-is_default', '-created')
            address_list = []
            for addr in addresses:
                address_list.append({
                    'id': addr.id,
                    'name': addr.name,
                    'phone': addr.phone,
                    'province': addr.province,
                    'city': addr.city,
                    'district': addr.district,
                    'detail': addr.detail,
                    'is_default': addr.is_default
                })
            return JsonResponse({'success': True, 'addresses': address_list})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class ProfileView(View):
    def get(self, request):
        active_tab = request.GET.get('tab', 'orders')
        
        user = get_current_user(request)
        user_id = user.id if user else 0
        
        orders = []
        addresses = []
        collections = []
        
        if active_tab == 'orders':
            orders = self.get_orders(request)
        elif active_tab == 'addresses':
            addresses = AddressInfos.objects.filter(user_id=user_id).order_by('-is_default', '-created')
        elif active_tab == 'collections':
            collections = CommodityInfos.objects.filter(likes__gt=0)[:10]
        
        return render(request, 'profile.html', {
            'active_tab': active_tab,
            'orders': orders,
            'addresses': addresses,
            'collections': collections,
            'current_page': 'profile',
            'user': user
        })
    
    def get_orders(self, request):
        user = get_current_user(request)
        user_id = user.id if user else 0
        
        order_list = []
        
        orders = OrderInfos.objects.filter(user_id=user_id).order_by('-created')
        
        for order in orders:
            items = []
            order_items = OrderItem.objects.filter(order=order)
            
            for item in order_items:
                image_url = item.commodity.img.url if item.commodity.img else 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=baby%20product%20placeholder&image_size=square'
                items.append({
                    'name': item.commodity.name,
                    'price': item.price,
                    'quantity': item.quantity,
                    'image': image_url
                })
            
            order_list.append({
                'order_sn': order.order_sn,
                'status': order.status_text,
                'status_text': order.status_text,
                'total_price': order.price,
                'total_count': sum(item.quantity for item in order_items),
                'items': items
            })
        
        return order_list


def login_page(request):
    return render(request, 'login.html')


def base(request):
    return render(request, 'base.html')
