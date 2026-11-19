
from django.contrib import admin
from django.urls import path, include
from files.views import dashboard


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('api/', include("files.urls")),
]
