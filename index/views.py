from django.shortcuts import render
from django.views import View
from commodity.models import CommodityInfos


class indexClassView(View):
    def get(self, request):
        today_hot = CommodityInfos.objects.order_by('-sold')[:8]
        
        clothing_types = ['童装', '配饰']
        baby_clothing = CommodityInfos.objects.filter(types__in=clothing_types).order_by('-sold')[:8]
        
        food_types = ['进口奶粉', '宝宝辅食', '营养品']
        baby_food = CommodityInfos.objects.filter(types__in=food_types).order_by('-sold')[:8]
        
        product_types = ['婴儿床', '纸尿裤', '婴儿车', '安全座椅', '婴儿湿巾', '儿童玩具']
        baby_products = CommodityInfos.objects.filter(types__in=product_types).order_by('-sold')[:8]

        return render(request, 'index.html', {
            'today_hot': today_hot,
            'baby_clothing': baby_clothing,
            'baby_food': baby_food,
            'baby_products': baby_products,
        })
