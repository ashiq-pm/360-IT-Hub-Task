from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('signout/', views.signout, name='signout'),
    path('home/', views.home, name='home'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('create/', views.create_service, name='create_service'),
    path('', views.service_list, name='service_list'),
    path('update/<int:pk>/', views.update_service, name='update_service'),
    path('delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('subscription/<int:service_id>/', views.subscription_view, name='subscription'),
    path('payment/success/', views.payment_success, name='payment_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)