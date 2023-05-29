from django.shortcuts import render, redirect, get_object_or_404
from .models import Annonces, Panier
from .annonce_form import AnnoncesForm, UsercreationForm, PanierForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def inscription_fonc(request):
    if request.method == 'POST':
        formulaire = UsercreationForm(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            return redirect('index_name')
    else:
        formulaire = UsercreationForm()
    return render(request, 'inscription.html', context={'formulaire': formulaire})


@login_required
def mes_annonces(request):
    if request.user.statut == 'Vendeur':
        annonces_utilisateur = Annonces.objects.filter(auteur_id=request.user.id)
        return render(request, 'mes_annonces.html', context={"annonces_utilisateur": annonces_utilisateur})
    return redirect('index_name')


@login_required
def ajout_annonce(request):
    if request.user.statut == 'Vendeur':
        if request.method == 'POST':
            formulaire = AnnoncesForm(request.POST, request.FILES)
            if formulaire.is_valid():
                nouvelle_annonce = formulaire.save(commit=False)
                nouvelle_annonce.enregistrer_avec_auteur(user_id=request.user.id)
                messages.success(request, 'Votre référence a été ajoutée avec succes')
                return redirect('index_name')
        else:
            formulaire = AnnoncesForm()
        return render(request, 'ajout_annonce.html', context={'formulaire': formulaire})


@login_required
def modifier_annonce(request, slug_modif_annonce):
    try:
        annonce = Annonces.objects.get(slug=slug_modif_annonce)
    except Annonces.DoesNotExist:
        return render('index_name')

    if request.method == 'POST':
        form = AnnoncesForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            form.save()
            return redirect('mes_annonces_name')
    else:
        form = AnnoncesForm(instance=annonce)
    return render(request, 'modif_annonce.html', context={'form': form})


@login_required
def supprimer_annonce(request, slug_suppression_annonce):
    try:
        annonce = Annonces.objects.get(slug=slug_suppression_annonce)
        if annonce.auteur == request.user:
            if request.method == 'POST':
                annonce.delete()
                messages.success(request, 'Votre annonce a été supprimée avec succès.')
                return redirect('mes_annonces_name')
            else:
                return render(request, 'supprimer_annonce.html', {'annonce': annonce})
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à supprimer cette annonce.")
            return redirect('mes_annonces_name')
    except Annonces.DoesNotExist:
        messages.warning(request, "L'annonce que vous essayez de supprimer n'existe pas.")
        return redirect('mes_annonces_name')


def details_panier(request):  # fourni toutes les information pour le panier du client connecte
    details_reference = []
    sous_total = 0
    panier = Panier.objects.filter(client_id=request.user.id)  # panier du client
    for annonce_panier in panier:
        details_reference.append({"ref": annonce_panier,
                                  'prix': annonce_panier.prix_reference(reference_id=annonce_panier.reference_id),
                                  'nombre_article': annonce_panier.quantite})
        sous_total = annonce_panier.montant_total_panier(user=request.user)
    return render(request, 'panier.html', context={'details_panier': details_reference,
                                                   'nombre_ref_panier': len(set(panier)),
                                                   'sous_total': sous_total})


def details_annonce(request, slug_request):  # Affiche detail de la ref + ajout dans le panier
    annonce = get_object_or_404(Annonces, slug=slug_request)
    user = request.user

    if request.method == 'POST':
        panier, created = Panier.objects.update_or_create(reference=annonce, client=user, defaults={'quantite': 1})  # Par défaut, la quantité est 1 si la référence n'existe pas dans le panier
        form = PanierForm(request.POST, instance=panier)  # pour enregistrer la quantité modifié par le client
        if form.is_valid():
            panier = form.save(commit=False)
            panier.save()
            messages.success(request, 'Votre panier a été modifié avec succès')
            return redirect('mon_panier_name')

    panier_client = Panier.objects.filter(client_id=user.id)
    if Panier.objects.filter(reference_id=annonce.id, client_id=user.id).exists():  # Vérifie si la référence est dans le panier du clients
        annonce_panier = Panier.objects.get(reference_id=annonce.id, client_id=user.id)
        return render(request, 'details_annonce.html', context={'annonce': annonce,
                                                                'choix_nombre_article': PanierForm(initial={"quantite": annonce_panier.quantite}),
                                                                'nombre_ref_panier': len(set(panier_client)),
                                                                'sous_total': Panier.montant_total_panier(user=request.user)})
    else:  # si la référence n'existe pas dans le panier on retourne un formulaire normale avc quantite egale 1 par defaut
        return render(request, 'details_annonce.html', context={'annonce': annonce,
                                                                'choix_nombre_article': PanierForm(),
                                                                'nombre_ref_panier': len(set(panier_client)),
                                                                'sous_total': Panier.montant_total_panier(user=request.user)})


def suppression_annonce_panier(request, slug_suppression_annonce_panier):
    try:
        annonce = Annonces.objects.get(slug=slug_suppression_annonce_panier)
        annonce_dans_pannier = Panier.objects.get(reference_id=annonce.id, client_id=request.user.id)
        annonce_dans_pannier.delete()
        messages.success(request, 'La reference a été supprimée avec succès')
        return redirect('mon_panier_name')
    except Annonces.DoesNotExist:
        messages.warning(request, 'Vous ne pouvez pas supprimer cette annonce')
        return redirect('mon_panier_name')
