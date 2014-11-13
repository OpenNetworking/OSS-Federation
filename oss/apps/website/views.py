from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.utils.decorators import method_decorator

from oss.apps.issuer.views import (issuer_create, IssuerDetailView,
                                   IssuerUpdateView,
                                   issuer_add_color, ColorDetailView)
from oss.apps.decorators import non_staff_required

import config

class HomeView(IssuerDetailView):
    """
    Custom DetailView for Issuer as the homepage of the website

    I want to use DetailView using current login user's pk instead of
    using keyword argument. So I override the get_object function.
    """

    template_name = "website/home.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk is None:
            pk = self.request.user.issuer.pk

        queryset = queryset.filter(pk=pk)

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    @method_decorator(non_staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomeView,
                     self).dispatch(request, *args, **kwargs)


class WebsiteIssuerUpdateView(IssuerUpdateView):

    template_name = 'website/issuer_update.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk is None:
            pk = self.request.user.issuer.pk

        queryset = queryset.filter(pk=pk)

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_success_url(self):
        return "/website/"

    @method_decorator(non_staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(WebsiteIssuerUpdateView,
                     self).dispatch(request, *args, **kwargs)

def signup(request):
    return issuer_create(request, template_name='website/signup.html',
                         redirect_to='/website/',
                         confirm=config.AUTO_CONFIRM_ISSUER_REGISTRATION)

def waiting(request):
    # ToDo: create a template
    return HttpResponse("""Thanks for your registration.\n
                        Wating for accepting...""")

@non_staff_required
def add_color(request):
    pk = request.user.issuer.pk
    redirect_to = '/website/'
    return issuer_add_color(request, pk,
                            template_name='website/add_color.html',
                            redirect_to=redirect_to,
                            confirm=config.AUTO_CONFIRM_COLOR_REGISTRATION)



class WebsiteColorDetailView(ColorDetailView):

    def get(self, request, *args, **kwargs):
        color = self.get_object()
        if color.issuer.pk != request.user.issuer.pk:
            raise Http404
        return super(WebsiteColorDetailView,
                     self).get(request, *args, **kwargs)

    @method_decorator(non_staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(WebsiteColorDetailView,
                     self).dispatch(request, *args, **kwargs)

