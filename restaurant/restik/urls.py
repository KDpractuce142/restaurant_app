from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.food_list, name='food_list'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('create_dish/', views.new_food, name='new_food'),
    path('dish/<int:id>/edit/', views.edit_food, name='edit_food'),
    path('del/<int:id>/', views.delete_food, name='del_food'),
    path('dishes/<category>/', views.filtered_food_list, name='food_cat'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
