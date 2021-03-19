from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'heroes', views.HeroViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'assets', views.AssetViewSet)
router.register(r'transactions', views.TransactionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', views.apiOverview, name="api-overview"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', obtain_auth_token, name='api_token_auth'),
    path('assets/<str:pk>/transactions', views.AssetView.as_view(), name="asset-transactions"),
    path('assets/<str:pk>', views.AssetView.as_view(), name="asset-detail"),
    path('users/<str:pk>', views.UserView.as_view(), name="user-detail"),
    path('transactions/<str:pk>', views.TransactionView.as_view(), name="transaction-detail")
]