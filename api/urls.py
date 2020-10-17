from django.urls import path,include
from .views import *
from rest_framework import routers

app_name = "api"
router = routers.DefaultRouter()

router.register('promo-controller', PromoCreateAndModifyView, basename='promo-controller')

urlpatterns = [
    path('', include(router.urls)),
    path('list', PromoListView.as_view(), name='list-promo'),
    path('consume-promo/<int:pk>/', PromoPointsView.as_view(), name='consume-promo'),]
