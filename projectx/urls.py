from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include


from .views import redirect_to_home  # Import your redirect view

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('base.urls')),
    path('api/v2/', include('Skill.urls')),

    # Add other app-specific routes here
]

# Catch-all pattern for redirecting to home on 404
re_path(r'^.*$', redirect_to_home),
