from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path("clients/", ClientsList.as_view(), name="clients"),
    path("client/<int:id>", ClientDetail.as_view(), name="client_detail"),
    path("client/<int:id>/up_del", ClientUpdateDelete.as_view(), name="client_update_delete"),

    path("debt/create", DebtCreateUpdateDelete.as_view(), name="debt_create"),
    path("debt/<int:id>", DebtCreateUpdateDelete.as_view(), name="debt"),

    path("base_info/", BaseInformations.as_view(), name="base_info"),
    path("search/", Search.as_view(), name="search"),

    path("csv/", getfile, name="csv")
]