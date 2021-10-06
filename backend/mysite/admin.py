from django.contrib import admin

from .models import Account, Division, ClubsLib, ClubsTable, ForwardsTable, Partner


class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'surname', 'patronymic', 'data_joined', 'last_login', 'is_admin',
                    'is_active', 'is_staff', 'is_superuser')


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ClubsLibAdmin(admin.ModelAdmin):
    list_display = ('name', 'division')


class ClubsTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'fio', 'year', 'photo')


class ForwardsTableAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'club', 'pucks', 'setups', 'penalty')


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'partner')


admin.site.register(Account, AccountAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(ClubsLib, ClubsLibAdmin)
admin.site.register(ClubsTable, ClubsTableAdmin)
admin.site.register(ForwardsTable, ForwardsTableAdmin)
admin.site.register(Partner, PartnerAdmin)
