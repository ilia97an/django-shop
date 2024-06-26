from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'), 
  path('gpus/', views.GPUListView.as_view(), name='gpus'), 
  path('cpus/', views.CPUListView.as_view(), name='cpus'), 
  path('producers/', views.ManufacturerListView.as_view(), name='producers'), 
  path('gpu/<int:pk>', views.GPUDetailView.as_view(), name='gpu-detail'), 
  path('cpu/<int:pk>', views.CPUDetailView.as_view(), name='cpu-detail'), 
  path('producer/<int:pk>', views.ManufacturerDetailView.as_view(), name='producer-detail'), 
  path('user/', views.DetailUser.as_view(), name='user-detail'),
  path('orders/', views.ListCart.as_view(), name='cart-list'), 
  path('product/<int:pk>/order', views.order_product, name='order_product'), 
  path('addcpu/', views.add_cpu, name='addcpu'), 
  path('rate/<int:product_id>/<int:rating>/', views.rate), 
]

#Cart urls
#

#urlpatterns += [
#  path('cart/', views.ListCart.as_view(), name='list-carts'),
#  path('cart/<int:pk>/', views.DetailCart.as_view(), name='detail-cart'),
#  path('cart/create/', views.CreateCart.as_view(), name='create-cart'),
#  path('cart/<int:pk>/update/', views.UpdateCart.as_view(), name='update-cart'),
#  path('cart/<int:pk/delete/', views.DeleteCart.as_view(), name='delete-cart'),
#]

#CartItem urls


#urlpatterns += [
#  path('cartitem/', views.ListCartItem.as_view(), name='list-cartitems'),
#  path('cartitem/<int:pk>/', views.DetailCartItem.as_view(), name='detail-cartitem'),
#  path('cartitem/create/', views.CreateCartItem.as_view(), name='create-cartitem'),
#  path('cartitem/<int:pk>/update/', views.UpdateCartItem.as_view(), name='update-cartitem'),
#  path('cartitem/<int:pk/delete/', views.DeleteCartItem.as_view(), name='delete-cartitem'),
#]
