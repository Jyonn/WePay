"""WePay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import urls
from django.conf.urls import url, static
# from django.contrib import admin
from django.views.generic import RedirectView
from WePay.settings import STATIC_DIR_URL

from . import router

index_view = RedirectView.as_view(url='/index.html', permanent=True)

urlpatterns = [
    # url(r'^favicon\.ico$', favicon_view),
    # url(r'^admin/', admin.site.urls),
    url(r'^$', index_view),
    url(r'^session$', router.session),
    url(r'^user$', router.user),
    url(r'^user/address$', router.user_address),
    url(r'^card$', router.card),
    url(r'^user/default-card$', router.user_default_card),
    url(r'^card/(?P<card_id>\d+)$', router.card_card_id),
    url(r'^category$', router.category),
    url(r'^category/(?P<category_id>\d+)/good$', router.category_category_id_good),
    url(r'^good$', router.good),
    url(r'^good/(?P<good_id>\d+)$', router.good_good_id),
    url(r'^button$', router.button),
    url(r'^button/(?P<button_id>\d+)$', router.button_button_id),
    url(r'^order$', router.order),
    url(r'^order?status=(?P<status>\w+)&page=(?P<page>\d+)&count=(?P<count>\d+)$', router.order_status_page_count),
    url(r'^order/(?P<order_id>\d+)/status$', router.order_order_id_status),
    url(r'^\w+$', index_view),
]

urlpatterns += static.static('/', document_root=STATIC_DIR_URL)
# urls.handler404 = index_view
