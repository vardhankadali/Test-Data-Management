import django_filters
from .models import *

class RequestFilter(django_filters.FilterSet):

    class Meta:
        model = Request
        fields = ('status',)
