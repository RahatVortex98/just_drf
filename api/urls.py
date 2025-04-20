from django.urls import path,include
from .views import index,person,login,PersonApiView,PersonViewset,RegsiterApiView,LoginAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('people',PersonViewset, basename="pepole")



urlpatterns = [

    path('',include(router.urls)),
    
    path('',index,name='index'),
    path('person/',person,name='person'),
    path('login/',login,name='login'),
    path('persons/',PersonApiView.as_view(),name="persons"),

    path('register/',RegsiterApiView.as_view(),name="register"),
    path('login/',LoginAPIView.as_view(),name="login"),


]
