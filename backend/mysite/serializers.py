from .models import Account, Division, ClubsLib, ClubsTable, ForwardsTable, Partner
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'email', 'surname', 'first_name', 'patronymic', 'password')


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ('id', 'name', )


class ClubsLibSerializer(serializers.ModelSerializer):
    division = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Division.objects.all(),
    )

    class Meta:
        model = ClubsLib
        fields = ('id', 'name', 'division', )


class ClubsTableSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ClubsLib.objects.all(),
    )

    class Meta:
        model = ClubsTable
        fields = ('id', 'name', 'fio', 'year', 'photo', )


class ForwardsTableSerializer(serializers.ModelSerializer):
    club = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ClubsLib.objects.all(),
    )

    class Meta:
        model = ForwardsTable
        fields = ('id', 'last_name', 'club', 'pucks', 'setups', 'penalty')


class PartnerSerializer(serializers.ModelSerializer):
    partner = serializers.SlugRelatedField(
        slug_field='last_name',
        queryset=ForwardsTable.objects.all(),
    )

    class Meta:
        model = Partner
        fields = ('id', 'last_name', 'partner')
