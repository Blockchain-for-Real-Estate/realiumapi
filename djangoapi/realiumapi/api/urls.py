from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tokens', views.TokenViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'properties', views.PropertyViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', views.apiOverview, name="api-overview"),
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', obtain_auth_token, name='api_token_auth'),
    # path('tokens/', views.TokenView.as_view()),
    # path('assets/<str:pk>/transactions', views.AssetView.as_view(), name="asset-transactions"),
    # path('tokens/<str:pk>', views.TokenView.as_view(), name="put"),
    # path('users/<str:pk>', views.UserView.as_view(), name="user-detail"),
    path('users/', views.UserView.as_view()),
    path('properties/', views.PropertyView.as_view()),
    path('register/', views.RegisterView.as_view()),
    # path('transactions/<str:pk>', views.TransactionView.as_view(), name="transaction-detail")
    # path('events/', views.EventView.as_view())
]