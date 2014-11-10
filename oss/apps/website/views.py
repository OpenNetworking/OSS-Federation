from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from oss.apps.issuer.views import (issuer_create, IssuerDetailView,
                                   issuer_add_color)
from oss.apps.decorators import non_staff_required

import config
# Create your views here.

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

        if pk is not None:
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


