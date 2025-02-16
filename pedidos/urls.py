from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.menu, name='menu'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:pizza_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:index>/', views.remover_carrinho, name='remover_carrinho'),
    path('pizza/<int:pizza_id>/', views.pizza_detalhes, name='pizza_detalhes'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
