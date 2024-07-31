from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('other/<str:month_id>/',views.other, name='other'),
    path('add_month/', views.addMonth, name = 'addentry'),
    path('edit_month/<str:pk>',views.editMonth, name = 'editmonth'),
    path('add_entries',views.addEntries, name = 'addentries'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_movimiento/<str:pk>', views.editEntry, name = 'editMovimiento'),
    path('comparar/',views.comparar, name = 'comparar')
]