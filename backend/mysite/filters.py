import rest_framework_filters as filters
from .models import Division, ClubsLib, ClubsTable, ForwardsTable


class DivisionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')


class ClubsLibFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    division = filters.RelatedFilter(DivisionFilter, queryset=Division.objects.all())

    class Meta:
        model = ClubsLib
        fields = {'division': ['exact', 'in']}


class ClubsTableFilter(filters.FilterSet):
    name = filters.RelatedFilter(ClubsLibFilter, queryset=ClubsLib.objects.all())
    fio = filters.CharFilter(field_name='fio', lookup_expr='icontains')
    year = filters.NumberFilter(field_name='year', lookup_expr='icontains')

    class Meta:
        model = ClubsTable
        fields = {'name': ['exact', 'in']}


class ForwardsTableFilter(filters.FilterSet):
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    club = filters.RelatedFilter(ClubsLibFilter, queryset=ClubsLib.objects.all())
    pucks = filters.NumberFilter(field_name='pucks', lookup_expr='icontains')
    setups = filters.NumberFilter(field_name='setups', lookup_expr='icontains')
    penalty = filters.DurationFilter(field_name='penalty', lookup_expr='icontains')

    class Meta:
        model = ForwardsTable
        fields = {'club': ['exact', 'in']}


class PartnerFilter(filters.FilterSet):
    last_name = filters.RelatedFilter(ForwardsTableFilter, queryset=ForwardsTable.objects.all())