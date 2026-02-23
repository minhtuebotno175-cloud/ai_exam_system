from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Core
    path('', include('apps.core.urls')),

    # Users
    path('users/', include('apps.users.urls')),

    # Documents
    path('documents/', include('apps.documents.urls')),

    # Quizzes
    path('quizzes/', include('apps.quizzes.urls')),

    # Exports
    path('exports/', include('apps.exports.urls')),
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
