"""Citadel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/wallet/', include('wallet.urls')),
    path('api/transaction/', include('transaction.urls')),
    path('api/bulk-requests/', include('bulk_requests.urls')),
    path('api/', include('polls.urls')),
]

env = os.environ.get('DJANGO_ENVIRONMENT', None)
if env == 'dev':
    urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
elif env == 'prod':
    pass
else:
    # no docker config urls
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns.extend([
        path('silk/', include('silk.urls', namespace='silk')),
        path('favicon.ico', RedirectView.as_view(url="/static/favicon.ico")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
