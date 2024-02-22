from django.views import generic
from catalog import models


class ContactsListView(generic.ListView):
    model = models.Contacts
    extra_context = {
        'title': 'Контакты'
    }

