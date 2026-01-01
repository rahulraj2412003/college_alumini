from django.views.static import serve 
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
]

# Add this to serve media files in production (Render) 
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
