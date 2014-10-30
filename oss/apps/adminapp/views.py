from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.contrib.admin.forms import AdminAuthenticationForm
from django.utils.decorators import method_decorator
from oss.apps.issuer.models import Issuer
from oss.apps.issuer.views import (IssuerDetailView, issuer_create,
                                   IssuerListView,
                                   UnconfirmedIssuerListView,
                                   issuer_add_color, issuer_update_color)
from oss.apps.decorators import staff_required


@staff_required
def index(request):
    return render(request, 'adminapp/index.html')

@staff_required
def admin_issuer_create(request):
    print 'admin_issuer_create'
    return issuer_create(request,
                         template_name='adminapp/issuer_create.html',
                         redirect_to='/adminapp/issuer_list/',
                         confirm=True)

@staff_required
def admin_issuer_add_color(request, pk):
    redirect_to = '/adminapp/issuer_detail/{0}/'.format(pk)
    return issuer_add_color(request, pk,
                             template_name='adminapp/issuer_add_color.html',
                             redirect_to=redirect_to)

def admin_issuer_update_color(request, issuer_pk, color_pk):
    redirect_to = '/adminapp/issuer_detail/{0}/'.format(issuer_pk)
    return issuer_update_color(request, issuer_pk, color_pk,
                               template_name='adminapp/issuer_update_color.html',
                               redirect_to=redirect_to)


class AdminIssuerDetailView(IssuerDetailView):

    template_name = 'adminapp/issuer_detail.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminIssuerDetailView,
                     self).dispatch(request, *args, **kwargs)

class AdminIssuerListView(IssuerListView):

    template_name = 'adminapp/issuer_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminIssuerListView,
                     self).dispatch(request, *args, **kwargs)


class AdminUnconfirmedIssuerListView(UnconfirmedIssuerListView):

    template_name = 'adminapp/unconfirmed_issuer_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminUnconfirmedIssuerListView,
                     self).dispatch(request, *args, **kwargs)


'''
@staff_required
@require_http_methods(['POST',])
def polis_owner_confirm(request, pk):
    try:
        polis_owner = PolisOwner.objects.get(pk=pk)
    except PolisOwner.DoseNotExist:
        raise Http404
    polis_owner.user.is_active = True
    polis_owner.user.save()
    if request.is_ajax():
        return HttpResponse()
    return HttpResponse()

@staff_required
@require_http_methods(['POST',])
def polis_owner_create(request):
    form = PolisOwnerCreationForm()
    if request.method == "POST":
        form = PolisOwnerCreationForm(request.POST)
        if form.is_valid():
            polis_owner = form.save()
            polis_owner.active()
            return HttpResponseRedirect(reverse('adminapp:polis_list'))

    return render(request, 'adminapp/polis_owner_create.html', dict(form=form))

'''
