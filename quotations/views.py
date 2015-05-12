from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from rest_framework import viewsets

from quotations import models as quotation_models, serializers
from libs import query_set


def _search_quotations(search_terms):
    quotation_query = Q()
    author_query = Q()
    for search_term in search_terms:
        quotation_query = quotation_query & Q(text__icontains=search_term)
        author_query = author_query & Q(author__name__icontains=search_term)
    quotations = quotation_models.Quotation.objects.filter(quotation_query | author_query)
    return quotations


class QuotationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuotationSerializer

    def get_queryset(self):
        quotations = _search_quotations(self.request.GET.getlist('search', ''))
        if self.request.GET.get('random', False):
            quotations = query_set.get_random(quotations)
        return quotations


def redirect_to_random(request):
    quotations = query_set.get_random(quotation_models.Quotation.objects.all())
    return redirect(quotations[0])


def list_quotations(request):
    search_text = request.GET.get('search_text', '').strip()
    quotations = _search_quotations(search_text.split())

    paginator = Paginator(quotations, settings.MAX_PER_PAGE)

    page = request.GET.get('page')
    try:
        quotations = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        quotations = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        quotations = paginator.page(paginator.num_pages)

    return render_to_response('quotations/show.html',
                              {'quotations': quotations,
                               'pages': [i for i in range(1, paginator.num_pages+1)],
                               'search_text': search_text},
                              context_instance=RequestContext(request))


def show_quotation(request, pk):
    quotations = quotation_models.Quotation.objects.filter(pk=pk)
    return render_to_response('quotations/show.html',
                              {'quotations': quotations,
                               'pages': [1]},
                              context_instance=RequestContext(request))
