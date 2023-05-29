from django.shortcuts import render
from data.models import Annonces, Panier
from django.core.paginator import Paginator


def index_page(request):
    try:
        search = request.GET.get('search')
        all_annonces = Annonces.objects.filter(titre__icontains=search).order_by("-date_pub")

    except ValueError:
        all_annonces = Annonces.objects.all().order_by("-date_pub")

    nombre_article = all_annonces.count()
    paginator = Paginator(all_annonces, 8)
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)

    panier_client = Panier.objects.filter(client_id=request.user.id)
    return render(request, 'index.html', context={"page_object": page_object,
                                                  'nombre_ref_panier': len(set(panier_client)),
                                                  'sous_total': Panier.montant_total_panier(user=request.user),
                                                  'nombre_article': nombre_article})
