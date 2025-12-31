# events/admin.py
from django.contrib import admin
from .models import Event,EventRegistration,Feedback

admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(Feedback)
