from django.urls import path
from . import views, contact_global
from django.contrib.auth import views as auth_views
from .forms import EmailValidationOnForgotPassword
from .sitemaps import StaticViewSitemap
from .models import *
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap

sitemaps = {
    'destination-details': GenericSitemap({
        'queryset': Destination.objects.all(), 'date_field': 'modified_date',
    }, priority=0.9, changefreq='monthly', ),

    'descat-details': GenericSitemap({
        'queryset': Destination_Category.objects.all(), 'date_field': 'modified_date',
    }, priority=0.9, changefreq='monthly', ),

    'blogz-details': GenericSitemap({
        'queryset': BlogData.objects.all(), 'date_field': 'modified_date',
    }, priority=0.9, changefreq='monthly', ),

    'vacancy-details': GenericSitemap({
        'queryset': Vacancy.objects.all(), 'date_field': 'modified_date',
    }, priority=0.9, changefreq='monthly', ),

    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('vacancylist', views.vacancylist, name='vacancylist'),
    path('bookinglist', views.bookinglist, name='bookinglist'),
    # path('generate-pdf', views.generate_pdf, name='generate-pdf'),
    path('generate-excel', views.export_applicant_xls, name='generate-excel'),

    path('reset-password/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword,
                                                                 template_name='pages/password-reset/reset-password.html'),
         name='reset-password'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
    (template_name='pages/password-reset/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view
    (template_name='pages/password-reset/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_done/', auth_views.PasswordChangeDoneView.as_view
    (template_name='pages/password-reset/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='pages/password-reset/password_reset_complete.html'),
         name='password_reset_complete'),

    path('user_logout', views.user_logout, name='user_logout'),
    path('destination', views.destination, name='destination'),
    path('destination-details/<slug:criteria>', views.destination_details, name='destination-details'),
    path('blogz', views.blogz, name='blogz'),
    path('blogz-details/<slug:criteria>', views.blogz_details, name='blogz-details'),
    path('vacancy', views.vacancy, name='vacancy'),
    path('vacancy-details/<slug:criteria>', views.vacancy_details, name='vacancy-details'),
    path('descat-details/<slug:criteria>', contact_global.descat_details, name='descat-details'),
    path('search', views.search, name='search'),
    # path('sign-up', contact_global.newsletter_signup, name='newsletter_signup'),
    path('unsubscribe', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('newsletter-post', views.control_newsletter, name='newsletter-post'),
    path('booking-edit/<int:pk>', views.UpdateBookingList.as_view(), name='booking-edit'),
    path('covid19nepal', views.covid19, name='covid19nepal'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]
