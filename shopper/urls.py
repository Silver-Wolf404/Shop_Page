from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('base/', views.base, name='base'),
    path('add/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update/', views.UpdateCartQuantityView.as_view(), name='update_cart'),
    path('delete/', views.DeleteCartItemView.as_view(), name='delete_cart_item'),
    path('clear/', views.ClearCartView.as_view(), name='clear_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('address/add/', views.AddAddressView.as_view(), name='add_address'),
    path('address/delete/', views.DeleteAddressView.as_view(), name='delete_address'),
    path('address/default/', views.SetDefaultAddressView.as_view(), name='set_default_address'),
    path('address/list/', views.GetAddressesView.as_view(), name='get_addresses'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('order/create/', views.CreateOrderView.as_view(), name='create_order'),
    path('order/success/', views.OrderSuccessView.as_view(), name='order_success'),
]
