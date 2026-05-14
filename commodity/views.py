from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from commodity.models import CommodityInfos


def commodity(request):
    page = request.GET.get('page', 1)
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'sold_desc')
    search_query = request.GET.get('q', '')
    
    products = CommodityInfos.objects.all()
    
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(types__icontains=search_query))
    
    if category:
        products = products.filter(types=category)
    
    if sort == 'sold_desc':
        products = products.order_by('-sold')
    elif sort == 'sold_asc':
        products = products.order_by('sold')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'new_desc':
        products = products.order_by('-created')
    elif sort == 'new_asc':
        products = products.order_by('created')
    elif sort == 'likes_desc':
        products = products.order_by('-likes')
    elif sort == 'likes_asc':
        products = products.order_by('likes')
    
    paginator = Paginator(products, 6)
    
    try:
        product_list = paginator.page(page)
    except Exception:
        product_list = paginator.page(1)
    
    return render(request, 'commodity.html', {
        'product_list': product_list,
        'total_count': paginator.count,
        'current_category': category,
        'current_sort': sort,
        'search_query': search_query
    })


def detail(request, id):
    product = get_object_or_404(CommodityInfos, id=id)
    
    hot_products = CommodityInfos.objects.exclude(id=id).order_by('-sold')[:6]
    
    return render(request, 'detail.html', {
        'product': product,
        'hot_products': hot_products
    })
