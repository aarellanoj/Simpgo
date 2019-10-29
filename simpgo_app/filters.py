import django_filters as df

from .models import Ticket

class TicketFilter(df.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'id': ['exact', ],
            'title': ['icontains', ],
        }

