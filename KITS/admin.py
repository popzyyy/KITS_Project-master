from django.contrib import admin
from .models import Study, KitOrder, KitInstance, Kit, Location, Requisition
from simple_history.admin import SimpleHistoryAdmin
from .models import UserHistory


class KitInstanceInline(admin.TabularInline):
    model = KitInstance
    extra = 0


@admin.register(Kit)
class KitList(admin.ModelAdmin):
    list_display = ('id', 'IRB_number', 'type_name', 'description')
    inlines = [KitInstanceInline]


@admin.register(KitInstance)
class KitInstanceAdmin(admin.ModelAdmin):
    list_display = ('kit', 'scanner_id', 'expiration_date')
    list_filter = ('expiration_date', 'kit')
    fieldsets = (
        (None, {
            'fields': ('kit', 'id',)
        }),
        ('Availability', {
            'fields': ('status', 'expiration_date')
        }),
    )


@admin.register(Location)
class LocationList(admin.ModelAdmin):
    list_display = ('building', 'room', 'shelf_number', )
#    list_filter = ('building', 'room')
#    search_fields = ('building', )
#    ordering = ['building']


@admin.register(KitOrder)
class KitOrderList(admin.ModelAdmin):
    list_display = ('type', 'link', 'description')
    list_filter = ('type', 'link')
    search_fields = ('type', )
    ordering = ['type']


@admin.register(Requisition)
class RequisitionList(admin.ModelAdmin):
    list_display = ('type', 'link', 'description')
    list_filter = ('type', 'link')
    search_fields = ('type',)
    ordering = ['type']

# @admin.register(Study)
# class StudyList(admin.ModelAdmin):
#    list_display = ('id','IRB_number', 'pet_name', 'status')
#    list_filter = ('id','IRB_number', 'start_date')
#    ordering = ['IRB_number']


class StudyHistoryAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'IRB_number', 'pet_name', 'status')
    history_list_display = ["status"]


admin.site.register(Study, SimpleHistoryAdmin)


@admin.register(UserHistory)
class UserHistoryList(admin.ModelAdmin):
    list_display = ('user', 'changed_on', 'the_object', 'history_instance')
