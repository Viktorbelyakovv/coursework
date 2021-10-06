from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Account, Division, ClubsLib, ClubsTable, ForwardsTable, Partner
from .serializers import AccountSerializer, DivisionSerializer, ClubsLibSerializer, ClubsTableSerializer,\
    ForwardsTableSerializer, PartnerSerializer
from .filters import DivisionFilter, ClubsLibFilter, ClubsTableFilter, ForwardsTableFilter, PartnerFilter
from django_filters.rest_framework import DjangoFilterBackend


class AccountViewSet(viewsets.ModelViewSet):
    # Доступ для всех без токена (для регистрации)
    permission_classes = (AllowAny,)

    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.filter()
        return queryset

    @action(methods=['POST'], detail=False)
    def reguser(self, request):
        try:
            account = Account.objects.get(username=request.data['username'])
            return Response({"response": "User already exists"}, status=status.HTTP_304_NOT_MODIFIED)
        except Account.DoesNotExist:
            try:
                Account.objects.create_user(username=request.data['username'], email=request.data['email'],
                                    surname=request.data['surname'], first_name=request.data['first_name'],
                                    patronymic=request.data['patronymic'], password=request.data['password'])
            except:
                return Response({"response": "Error"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"response": "okay"}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def profile(self, request):
        try:
            account = Account.objects.get(username=request.query_params['user'])
        except Account.DoesNotExist:
            return Response({"response": "Error"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AccountSerializer(account)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=False)
    def editdata(self, request):
        try:
            account = Account.objects.get(username=request.data['username'])
        except Account.DoesNotExist:
            return Response({"response": "Account does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if account.check_password(request.data['password']):
            account.username = request.data['username2']
            account.email = request.data['email']
            account.surname = request.data['surname']
            account.first_name = request.data['first_name']
            account.patronymic = request.data['patronymic']
            account.save()
            return Response({"response": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"response": "Not correct password"}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['PATCH'], detail=False)
    def editpassword(self, request):
        try:
            account = Account.objects.get(username=request.data['username'])
        except Account.DoesNotExist:
            return Response({"response": "Account does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if account.check_password(request.data['passwordold']):
            account.set_password(request.data['password'])
            account.save()
            return Response({"response": "password set"}, status=status.HTTP_200_OK)
        else:
            return Response({"response": "Not correct password"}, status=status.HTTP_403_FORBIDDEN)


class DivisionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = DivisionSerializer
    # Класс, описывающий правила фильтрации
    filter_class = DivisionFilter
    filter_backends = (DjangoFilterBackend, )

    def get_queryset(self):
        queryset = Division.objects.filter()
        return queryset


class ClubsLibViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ClubsLibSerializer
    # Класс, описывающий правила фильтрации
    filter_class = ClubsLibFilter
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        queryset = ClubsLib.objects.filter()
        return queryset


class ClubsTableViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ClubsTableSerializer
    # Класс, описывающий правила фильтрации
    filter_class = ClubsTableFilter
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        queryset = ClubsTable.objects.filter()
        return queryset


class ForwardsTableViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ForwardsTableSerializer
    # Класс, описывающий правила фильтрации
    filter_class = ForwardsTableFilter
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        queryset = ForwardsTable.objects.filter()
        return queryset


class PartnerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PartnerSerializer
    filter_class = PartnerFilter
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        queryset = Partner.objects.all()
        return queryset
