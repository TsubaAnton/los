from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from user.forms import ProfileForm, ImageUploadForm
from user.models import User
from .models import Event, Article


def all_user_events(request):
    users = User.objects.filter(events__isnull=False).distinct()
    print(users)
    return render(request, 'los/all_user_events.html', {'all_users': users})


def articles_list(request):
    articles = Article.objects.all()
    return render(request, 'los/articles_list.html', {'articles': articles})


def event_list(request):
    events = Event.objects.all()
    return render(request, 'los/events_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = event.attendees.all()
    return render(request, 'los/events_detail.html', {'event': event, 'attendees': attendees})


def event_attend(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.attendees.add(request.user)
    return redirect(reverse('los:event_detail', args=[event_id]))


def profile_attend(request, user_id):
    user = User.objects.get(id=user_id)
    profile_form = ProfileForm(instance=user)
    image_form = ImageUploadForm(instance=user)

    return render(request, 'los/profile_link.html', {'current_user': user})
