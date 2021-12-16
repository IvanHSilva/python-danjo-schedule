from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from .models import Contact
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages

def index(request):
    contactlist = Contact.objects.order_by('-id').filter(
        active=True
    )
    paginator = Paginator(contactlist, 12)
    page = request.GET.get('p')
    contactlist = paginator.get_page(page)
    return render(request, 'contacts/index.html', {
        'contacts': contactlist
    })

def details(request, id):
    # contact = Contact.objects.get(id=id)
    contact = get_object_or_404(Contact, id=id)
    if contact.active:
        return render(request, 'contacts/details.html', {
            'contact': contact
        })
    else:
        raise Http404()

def search(request):
    text = request.GET.get('text')
    if text is None or not text:
        messages.add_message(request, messages.ERROR, 'Campo de pesquisa não pode ser vazio!')
        return redirect('index')

    fields = Concat('name', Value(' '), 'midname')
    contactlist = Contact.objects.annotate(
        compname=fields
    ).filter(
        Q(compname__icontains=text) | Q(phone__icontains=text)
    )
    # contactlist = Contact.objects.order_by('-id').filter(
    #     Q(name__icontains=text) | Q(midname__icontains=text),
    #     active=True
    # )
    # print(contactlist.query)
    paginator = Paginator(contactlist, 12)
    page = request.GET.get('p')
    contactlist = paginator.get_page(page)
    return render(request, 'contacts/search.html', {
        'contacts': contactlist
    })
