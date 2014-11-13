from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from oss.apps.decorators import staff_required

from .models import Issuer, Color, ColorHistory, Address, AddressHistory
from .forms import (IssuerCreationForm, IssuerUpdateForm,
                    ColorCreationForm, AddressInputForm)

def issuer_create(request, template_name='issuer/form.html',
                  redirect_to=None,
                  confirm=False):
    if request.method == "POST":
        issuer_form = IssuerCreationForm(request.POST)
        user_form = UserCreationForm(request.POST)
        user = None
        issuer = None

        if user_form.is_valid():
            user = user_form.save(commit=False)

        if issuer_form.is_valid():
            issuer = issuer_form.save(commit=False)

        if user and issuer:
            user.save()
            issuer.user = user
            issuer.save()
            if confirm:
                messages.success(request,
                                 'Success, you can login now!')
                issuer.active()
            else:
                messages.info(request, 'Wating for approve')
                issuer.deactive()

            if redirect_to:
                return HttpResponseRedirect(redirect_to)

            return HttpResponse('success')
    else:
        issuer_form = IssuerCreationForm()
        user_form = UserCreationForm()

    return render(request, template_name,
                  {'issuer_form': issuer_form,
                   'user_form': user_form})

def issuer_delete(request):
    return HttpResponse('delelte')

def issuer_add_color(request, issuer_pk, confirm=False,
                     template_name="issuer/issuer_add_color.html",
                     redirect_to=None):
    issuer = get_object_or_404(Issuer, pk=issuer_pk)
    if request.method == 'POST':
        color_form = ColorCreationForm(request.POST)
        address_form = AddressInputForm(request.POST)
        if color_form.is_valid() and address_form.is_valid():
            #create address
            raw_address = address_form.cleaned_data.get('address')
            address = Address(address=raw_address, issuer=issuer)
            address.save()

            color = color_form.save(commit=False)
            color.address = address
            color.issuer = issuer
            last_color = (Color.objects.all()
                                       .order_by('color_id').last())

            color_id = 1
            if last_color:
                color_id = last_color.color_id + 1
            color.color_id = color_id
            if confirm:
                messages.success(request,
                                 'add color success')
                color.is_confirmed = True
            else:
                messages.info(request,
                              'waiting for approve')

            color.save()

            if not redirect_to:
                redirect_to = '/issuer/{0}/detail/'.format(issuer_pk)

            return HttpResponseRedirect(redirect_to)
    else:
        color_form = ColorCreationForm()
        address_form = AddressInputForm()

    return render(request, template_name,
                  {'color_form': color_form, 'address_form': address_form,
                   'issuer': issuer })

class IssuerUpdateView(UpdateView):

    model = Issuer
    fields = ['register_url']
    template_name_suffix = '_update'

    def get_success_url(self):
        obj = self.get_object()
        return '/issuer/{0}/detail/'.format(obj.pk)

class IssuerDetailView(DetailView):

    model = Issuer

class IssuerListView(ListView):

    queryset = Issuer.objects.filter(user__is_active=True)
    context_object_name = 'issuer_list'

class UnconfirmedIssuerListView(ListView):

    queryset = Issuer.objects.filter(user__is_active=False)
    context_object_name = 'issuer_list'

class ColorListView(ListView):

    queryset = Color.objects.filter(is_confirmed=True)
    context_object_name = 'color_list'

class UnconfirmedColorListView(ListView):

    queryset = Color.objects.filter(is_confirmed=False)
    context_object_name = 'color_list'
    template_name = 'issuer/unconfirmed_color_list.html'

class ColorDetailView(DetailView):

    model = Color

class ColorHistoryListView(ListView):

    model = ColorHistory
    context_object_name = 'colorhistory_list'

class AddressHistoryListView(ListView):

    model = AddressHistory
    context_object_name = 'addresshistory_list'


