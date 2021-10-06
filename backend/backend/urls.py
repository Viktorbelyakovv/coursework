from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='home'),
    re_path(r'^api/', include('mysite.urls')),
    re_path(r'^api/token/', obtain_jwt_token),
    re_path(r'^api-token-verify/', verify_jwt_token),
    re_path(r'^api-token-refresh/', refresh_jwt_token),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)