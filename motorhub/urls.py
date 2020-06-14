from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns =[
    path('', views.home, name='home'),
    path('car_search', views.car_search, name='car_search'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.sign_up, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('payment', views.payment, name='payment'),
    path('<int:id>/view_car', views.view_car, name='view_car'),
    path('about', views.about, name='about'),
    path('settings', views.settings, name='settings'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
