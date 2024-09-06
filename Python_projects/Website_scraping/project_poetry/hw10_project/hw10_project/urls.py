from django.contrib import admin
from django.urls import path, include
from users import views as views_users
from quotes import views as views_quotes
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("quotes.urls")),
    path('signup/', views_users.signupuser, name='signup'),
    path('users/', include('users.urls')),
    #path('login/', views.login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', views_users.profile, name='profile'),
    path('add/', views_quotes.add_quote, name='add_quote'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

