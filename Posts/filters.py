from django.forms import DateTimeInput
from django.utils.translation import gettext as _
from django_filters import (
    FilterSet, DateTimeFilter, ModelChoiceFilter, CharFilter
)

from .models import Post, Role


class PostFilter(FilterSet):
    role = ModelChoiceFilter(
        field_name='role',
        queryset=Role.objects.all(),
    )
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
    )
    text = CharFilter(
        field_name='text',
        lookup_expr='icontains',
    )
    added_after = DateTimeFilter(
        label='Date',
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['role'].extra.update(
            {
                'empty_label': _('Any'),
            }
        )

    class Meta:
        model = Post

        fields = {}
