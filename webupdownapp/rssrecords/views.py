from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Rssrecord
from .forms import RssRecordsForm

class RssRecordList(ListView):
    model = Rssrecord
    paginate_by = 10
    template_name = 'rssrecords/rssrecord_list.html'
    context_object_name = 'rssrecords'

    def get_queryset(self):
        try:
            a = self.request.GET.get('rssrecord',)
        except KeyError:
            a = None
        if a:
            rssrecords_list = Rssrecord.objects.filter(
                name__icontains=a,
                owner=self.request.user
            )
        else:
            rssrecords_list = Rssrecord.objects.filter(owner=self.request.user)
        return rssrecords_list

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RssRecordList, self).dispatch(*args, **kwargs)

@login_required()
def account_detail(request, uuid):

    account = Account.objects.get(uuid=uuid)
    if account.owner != request.user:
            return HttpResponseForbidden()

    variables = {
        'account': account,
    }

@login_required()
def rssrecord_cru(request, uuid=None):

    if uuid:
        rssrecord = get_object_or_404(Rssrecord, uuid=uuid)
        if rssrecord.owner != request.user:
            return HttpResponseForbidden()
    else:
        rssrecord = Rssrecord(owner=request.user)

    if request.POST:
        form = RssRecordsForm(request.POST, instance=rssrecord)
        if form.is_valid():
            rssrecord = form.save(commit=False)
            rssrecord.owner = request.user
            rssrecord.save()
            redirect_url = reverse(
                'webupdownapp.rssrecords.views.rssrecord_detail',
                args=(rssrecord.uuid,)
            )
            return HttpResponseRedirect(redirect_url)
    else:
        form = RssRecordsForm(instance=rssrecord)

    variables = {
        'form': form,
        'rssrecord': rssrecord
    }

    template = 'rssrecords/rssrecord_cru.html'

    return render(request, template, variables)