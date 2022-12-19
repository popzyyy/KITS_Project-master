import django_filters
from .models import *


# from django.db.models import F


class StudyFilter(django_filters.FilterSet):
    class Meta:
        model = Study
        fields = (
            'IRB_number', 'pet_name', 'status',
        )


class KitFilter(django_filters.FilterSet):
    class Meta:
        model = Kit
        fields = (
            "IRB_number_id", 'type_name'
        )


class KitReportFilter(django_filters.FilterSet):
    class Meta:
        model = Kit
        # fields = 'IRB_number'
        fields = '__all__'
        exclude = 'description', 'date_added', 'type_name'


class KitInstanceFilter(django_filters.FilterSet):
    class Meta:
        model = KitInstance
        fields = '__all__'
        exclude = 'id', 'scanner_id', 'note', 'expiration_date', 'kit_id', 'location_id',


class StudyOnKitInstanceFilter(django_filters.FilterSet):
    class Meta:
        model = Study
        fields = 'pet_name', 'IRB_number',


class DateRangeFilter(django_filters.FilterSet):
    class Meta:
        model = KitInstance
        fields = '__all__'


class LocationFilter(django_filters.FilterSet):

    # building = django_filters.ChoiceFilter(choices=FILTER_CHOICES)
    class Meta:
        model = Location
        fields = '__all__'
        # fields = ['building', 'room']
