from django .urls import path
from .import views

urlpatterns = [
    path ('', views.homepage, name='homepage'), 
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-auction/', views.create_auction_view, name='create_auction'),
    path('auction/<int:auction_id>/', views.auction_detail_view, name='auction_detail'),
    path('my-auctions/', views.my_auctions_views, name='my_auctions'),
    path('edit-auction/<int:auction_id>/', views.edit_auction_view, name='edit_auction'),
    path('delete-auction/<int:auction_id>/', views.delete_auction_view, name='delete_auction'),
    path('bid-history/<int:auction_id>/', views.bid_history_view, name='bid_history'),
]