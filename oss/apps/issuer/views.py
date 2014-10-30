from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from .models import Issuer, Color, HistoryAddress
from .forms import (IssuerCreationForm, ColorCreationForm,
                    ActiveAddressCreationForm)
from oss.apps.decorators import staff_required
from django.views.generic import ListView, DetailView

def issuer_create(request, template_name='issuer/form.html',
                  redirect_to=None,
                  confirm=False):
    issuer_form = IssuerCreationForm()
    user_form = UserCreationForm()
    if request.method == "POST":
        issuer_form = IssuerCreationForm(request.POST)
        user_form = UserCreationForm(request.POST)
        user = None
        issuer = None

        if user_form.is_valid():
            user = user_form.save(commit=False)
            print('user form valid')

        if issuer_form.is_valid():
            issuer = issuer_form.save(commit=False)
            print('issuer form valid')

        if user and issuer:
            user.save()
            issuer.user = user
            issuer.save()
            if confirm:
                issuer.active()
            if redirect_to:
                return HttpResponseRedirect(redirect_to)
            return HttpResponse('success')

    return render(request, template_name,
                  {'issuer_form': issuer_form,
                   'user_form': user_form})

def issuer_delete(request):
    return HttpResponse('delelte')

def issuer_update(request):
    return HttpResponse('update')

def issuer_add_color(request, pk,
                     template_name="issuer/issuer_add_color.html",
                     redirect_to=None):

    issuer = get_object_or_404(Issuer, pk=pk)
    color_form = ColorCreationForm()
    address_form = ActiveAddressCreationForm()
    if request.method == 'POST':
        color_form = ColorCreationForm(request.POST)
        address_form = ActiveAddressCreationForm(request.POST)
        if color_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            color = color_form.save(commit=False)
            color.current_address = address
            color.issuer = issuer
            last_color = Color.objects.all() \
                                        .order_by('color_number').last()

            color_number = 1
            if last_color:
                color_number = last_color.color_number + 1
            color.color_number = color_number
            color.save()
            if not redirect_to:
                redirect_to = '/issuer/{0}/detail/'.format(pk)

            return HttpResponseRedirect(redirect_to)

    return render(request, template_name,
                  {'color_form': color_form, 'address_form': address_form,
                   'issuer': issuer })

def issuer_update_color(request, issuer_pk, color_pk,
                        template_name="issuer/issuer_update_color.html",
                        redirect_to=None):
    color = get_object_or_404(Color, pk=color_pk)
    issuer = get_object_or_404(Issuer, pk=issuer_pk)
    current_address = color.current_address
    address_form = ActiveAddressCreationForm()
    if request.method == "POST":
        address_form = ActiveAddressCreationForm(request.POST)
        if address_form.is_valid():

            # create history address
            history_address = HistoryAddress()
            history_address.address = current_address.address
            history_address.start_time = current_address.create_time
            history_address.color = color
            history_address.save()

            # create active address
            address = address_form.save()

            # update current address
            color.current_address = address
            color.save()

            # delete old address
            current_address.delete()

            if not redirect_to:
                redirect_to = '/issuer/{0}/detail/'.format(issuer_pk)

            return HttpResponseRedirect(redirect_to)


    return render(request, template_name,
                  {'address_form': address_form,
                   'issuer': issuer,
                   'color': color })

class IssuerDetailView(DetailView):

    model = Issuer

class IssuerListView(ListView):
    queryset = Issuer.objects.filter(user__is_active=True)
    context_object_name = 'issuers'

    def dispatch(self, *args, **kwargs):
        return super(IssuerListView, self).dispatch(*args, **kwargs)

class UnconfirmedIssuerListView(ListView):
    queryset = Issuer.objects.filter(user__is_active=False)
    context_object_name = 'issuers'
    def dispatch(self, *args, **kwargs):
        return super(UnconfirmedIssuerListView,
                     self).dispatch(*args, **kwargs)


