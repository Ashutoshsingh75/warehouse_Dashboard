"""laundry_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from laundry import views
app_name="laundry"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name="home"),
    path("login/",views.user_login,name="login"),
    path("register/",views.register_user,name="register"),
    path("logout/",views.user_logout,name="logout"),
    path("laundry/",views.launder_user,name="laundry"),
    path("laundrycat/",views.launder_cat,name="laundrycat"),
    path("shop_details/<str:username>/",views.shop_details,name="shop_details"),
    path("order/<int:id>/<str:username>/",views.laundry_order,name="order"),
    path("order_final/<int:id>/<str:shopname>/",views.laundry_order_final,name="order_final"),
    path("delete/<str:cat>/<int:id>/<str:username>/",views.delet_cart,name="delete"),
    path("pay/<str:shopname>/<int:shopid>/",views.payment,name="pay"),
    path("online_payment",views.payment,name="online_payment"),
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/<int:shopid>/<str:shopname>/',views.paymentSuccess),
    path('confirmation/',views.confirmationPage,name="confirmation"),
    path('user_order_list/',views.order_list_for_user,name="user_order_list"),
    path('shop_order_list/',views.order_list_for_shop,name="shop_order_list"),
    path('after_order_pay/<int:id>',views.after_oredr_pay,name="after_order_pay"),
    path('paymentSuccess_after_pay/<str:rppid>/<str:rpoid>/<str:rpsid>/<int:oder_id>/',views.paymentSuccess_after_order),
    path("profile/",views.update_profile,name="profile"),
    path("updatepass/",views.change_password,name="updatepass"),
    path("orderupdate/<int:order_id>/",views.order_update,name="orderupdate"),
     path("shopprofile/",views.shop_profile,name="shopprofile"),



]
# ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
