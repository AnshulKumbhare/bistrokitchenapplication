from bistrokitchen_app import views
from django.urls import path
from bistrokitchen import settings
from django.conf.urls.static import static


urlpatterns = [
    path('header', views.header),
    path('footer', views.footer),
    path('home', views.home),
    path('register', views.register),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('menu', views.menu),
    path('menufilter/<mf>', views.menufilter),
    path('pricefilter/<pf>', views.pricefilter),
    path('minmaxrange', views.minmaxrange),
    path('menudetails/<mdid>', views.menudetails),
    path('addtocart/<mdid>', views.addtocart),
    path('viewcart', views.viewcart),
    path('updateqty/<qv>/<cid>', views.updateqty),
    path('remove/<cid>', views.remove),
    path('placeorder', views.placeorder),
    path('removeorder/<o_id>', views.removeorder),
    path('contactus', views.contactus),
    path('chefs', views.chefs),
    path('makepayment', views.makepayment),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

    