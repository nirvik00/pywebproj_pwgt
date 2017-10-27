from django.contrib import admin
from .models import Adj, RawData, Node


# Register your models here.

admin.site.register(Adj)
admin.site.register(RawData)
admin.site.register(Node)