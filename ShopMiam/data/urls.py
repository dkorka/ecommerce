from django.urls import path
from .views import mes_annonces, ajout_annonce, inscription_fonc,details_annonce, details_panier,suppression_annonce_panier, supprimer_annonce,modifier_annonce
from django.contrib.auth import views as auth_views
from .api_data import api_data



urlpatterns = [
    path('mes_annonces/',mes_annonces,name='mes_annonces_name'),
    path('mes_annonces/modifier/<slug:slug_modif_annonce>', modifier_annonce, name='modifier_annonce_name'),
    path('mes_annonces/<slug:slug_suppression_annonce>',supprimer_annonce, name='suppression_annonce_name'),
    path('ajout_annonce/',ajout_annonce,name='ajout_annonce_name'),
    path('api_data/',api_data),
    path('inscription/',inscription_fonc,name='inscription_name'),
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='logged_out.html'), name="logout"),
    path('<slug:slug_request>',details_annonce,name='details_name'),
    path('panier/',details_panier, name="mon_panier_name"),
    path('panier/<slug:slug_suppression_annonce_panier>',suppression_annonce_panier, name="suppression_annonce_panier_name"),
]

# from django.contrib.auth import urls