from django.urls import path
from .views import RegisterView, CompanyListView, WatchlistView, AddToWatchlist, RemoveFromWatchlist
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('companies/', CompanyListView.as_view(), name='companies'),
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/add/', AddToWatchlist.as_view(), name='watchlist_add'),
    path('watchlist/remove/', RemoveFromWatchlist.as_view(), name='watchlist_remove'),
]
