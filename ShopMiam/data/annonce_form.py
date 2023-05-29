
from django.forms import ModelForm
from .models import Annonces, Usercreation, Panier
from django.contrib.auth.forms import UserCreationForm


class UsercreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usercreation
        fields = UserCreationForm.Meta.fields + ('email', 'last_name', 'age', 'statut')


class AnnoncesForm(ModelForm):
    class Meta:
        model = Annonces
        fields = ['slug', 'titre', 'description', 'piece_jointe', 'prix']


class PanierForm(ModelForm):
    class Meta:
        model = Panier
        fields = ['quantite']
