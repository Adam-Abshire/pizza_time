from django.urls import path
from . import views

urlpatterns = [
    path('', views.registration),
    path('login', views.login),
    path('menu', views.menu),
    path('cart/<int:pizza_id>', views.cart),
    path('success/<int:pizza_id>', views.success),
    path('login_user', views.login_user),
    path('register_user', views.register),
    path('user/<int:member_id>', views.specific_user),
    path('logout', views.logout),
    path('edit/<int:member_id>', views.edit_user),
    path('create_pizza', views.create_pizza),
    path('favorite/<int:pizza_id>', views.favorite),
    path('unfavorite/<int:pizza_id>', views.unfavorite),
    path('reorder/<int:pizza_id>', views.reorder),
    path('make_edits/<int:member_id>', views.make_edits),
]