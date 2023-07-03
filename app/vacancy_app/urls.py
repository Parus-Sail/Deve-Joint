from django.urls import path
from django.views.generic import RedirectView
from vacancy_app import views

from .apps import VacancyAppConfig

app_name = VacancyAppConfig.name

urlpatterns = [
    path("", RedirectView.as_view(url="job-listing")),
    path("job-listing/", views.JobsListingView.as_view(), name="job-listing"),
    path("job-details/", views.JobsDetailView.as_view(), name="job-details"),
    # Payment Account url
    path('payment-account/', views.PaymentAccountListView.as_view(), name='payment_account_list'),
    path('payment-account/<int:pk>/detail/', views.PaymentAccountDetailView.as_view(), name='payment_account_detail'),
    path('payment-account/create/', views.PaymentAccountCreateView.as_view(), name='payment_account_create'),
    path('payment-account/<int:pk>/update/', views.PaymentAccountUpdateView.as_view(), name='payment_account_update'),
    path('payment-account/<int:pk>/delete/', views.PaymentAccountDeleteView.as_view(), name='payment_account_delete'),
    path("payment-account/<int:pk>/<str:status>/change-status/",
         views.PaymentAccountChangeStatus.as_view(),
         name="payment_account_change_status"),
    path("payment-account/moderation/",
         views.SearchResultPaymentAccountModerationListView.as_view(),
         name="payment_account_moderation_list"),
    path("payment-account/<int:pk>/moderation-update/",
         views.PaymentAccountModerationUpdateView.as_view(),
         name="payment_account_moderation_update"),
    path("profile/<int:pk>/detail/", views.UserProfileView.as_view(), name="user_profile_detail"),
    # Company url
    path('company/', views.CompanyListView.as_view(), name='company_list'),
    path('company/<int:pk>/detail/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('company/create/', views.CompanyCreateView.as_view(), name='company_create'),
    path('company/<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company_update'),
    path('company/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),
]
