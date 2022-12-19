from django import forms
from .models import KitInstance, Kit, Study, Location, Requisition, KitOrder, User


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = (
            'id', 'IRB_number', 'pet_name', 'comment', 'sponsor_name', 'status',
            'start_date', 'end_date')


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = '__all__'
        exclude = ('study',)


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = (
            'IRB_number', 'type_name', 'description', 'date_added', 'id',)


class KitIDForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ('id',)


class KitInstanceForm(forms.ModelForm):
    class Meta:
        model = KitInstance
        fields = '__all__'
        exclude = ('created_date', 'checked_out_date', 'status', 'kit',)
        # child_model = Kit
        # child_form_class = KitIDForm


class KitOrderForm(forms.ModelForm):
    class Meta:
        model = KitOrder
        fields = '__all__'
        exclude = ('study',)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class KitInstanceEditForm(forms.ModelForm):
    KIT_STATUS = (
        ('c', 'Checked Out'),
    )

    status = forms.TypedChoiceField(choices=KIT_STATUS, coerce=str, initial=1)

    class Meta:
        model = KitInstance
        fields = ("status",)


class KitInstanceDemolishForm(forms.ModelForm):
    KIT_STATUS = (
        ('d', 'Demolished'),
    )

    status = forms.TypedChoiceField(choices=KIT_STATUS, coerce=str, initial=1)

    class Meta:
        model = KitInstance
        fields = ['status']


class ExpiredReportDownloadForm(forms.ModelForm):
    KIT_STATUS = (
        ('e', 'Expired'),
    )

    status = forms.TypedChoiceField(choices=KIT_STATUS, coerce=str, initial=1)

    class Meta:
        model = KitInstance
        fields = ['scanner_id', 'expiration_date']

    class Meta1:
        model = Kit
        fields = ['type_name', 'IRB_number']


class UserReportForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class AllKitsForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = '__all__'


'''
    class Meta1:
        model = Kit
        fields = '__all__'

    class Meta2:
        model = KitInstance
        fields = '__all__'
'''