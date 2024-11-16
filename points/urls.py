from django.urls import path
from . import views

urlpatterns = [
    path('', views.google_auth_view, name='login'),  # landing page for login
    path('app/', views.index, name='index'),  # main app view (index)
    path('add-point/', views.add_point, name='add_point'),
    path('show-points/', views.show_points, name='show_points'),
    path('delete-point/<int:point_id>/', views.delete_point, name='delete_point'),
    path('check-geotag/', views.check_geotag, name='check_geotag'),
    path('logout/', views.logout_view, name='logout'),  # logout view
]
