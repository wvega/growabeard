# encoding: utf-8
from datetime import date, datetime
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campaign
from .forms import UploadForm


def index(request):
    campaign = Campaign.get_active()

    if not campaign:
        return render(request, 'no-campaign.html')

    return redirect('campaign-details', campaign.id)


@login_required
def upload(request):
    campaign = Campaign.get_active()

    if not campaign:
        return HttpResponseForbidden()

    today = date.today()

    if campaign.entries.filter(user=request.user, created_at__date=today).exists():
        messages.error(request, 'You\'ve already uploaded an image for today.')
        return redirect('/')

    form = UploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        campaign.entries.create(user=request.user, file=request.FILES['image'], created_at=datetime.now())
        messages.success(request, 'Thanks for sharing your beard progress!')
        return redirect('/')

    return render(request, 'upload.html', dict(form=form))


def campaign_details(request, id):
    campaign = get_object_or_404(Campaign, pk=id)
    return render(request, 'campaign.html', dict(campaign=campaign))
