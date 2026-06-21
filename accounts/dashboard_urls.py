from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("agent/", views.agent_dashboard, name="agent"),
    path("buyer/", views.buyer_dashboard, name="buyer"),
    path("seller/", views.seller_dashboard, name="seller"),
]
