from django.urls import path
from .views import identify_contact, all_contacts

urlpatterns = [
    path('identify/', identify_contact, name='identify_contact'),
    path('all-contacts/', all_contacts, name='all_contacts'),
]
