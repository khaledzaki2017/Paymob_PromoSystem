from core.models import Promo, User
from api import serializers

from rest_framework import generics
from rest_framework import viewsets

# from rest_framework.permissions import AllowAny
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser

import logging
logger = logging.getLogger('django')

from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers as ser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = []
        elif self.action == 'retrive' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class PromoCreateAndModifyView(viewsets.ModelViewSet):
    queryset = Promo.objects.all()
    serializer_class = serializers.PromoSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                promo_data = serializer.data
                logger.info("promo created from PromoCreateView")
                return Response(promo_data,
                                status=status.HTTP_201_CREATED)
            else:
                logger.error('Something went wrong in PromoCreateView !')
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

class PromoListView(generics.ListAPIView):
	serializer_class =serializers.PromoSerializer

	def get_queryset(self):
		return Promo.objects.all()
		user = User.objects.get(username=self.request.user)
		if user.is_staff is True:
			return Promo.objects.all()
		else:
			return Promo.objects.filter(user=user)


class PromoPointsView(generics.RetrieveUpdateAPIView):
    queryset = Promo.objects.all()
    serializer_class = serializers.PromoPointsSerializer
    permission_classes = [IsLoggedInUserOrAdmin]

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        promo = Promo.objects.filter(pk=pk)[0]
        if request.data['remaining_amount'] > promo.amount or request.data['remaining_amount'] < 0:
            raise ser.ValidationError("invalid promo points")
        request.data['amount'] = promo.amount - request.data['remaining_amount']
        request.data.pop('remaining_amount')

        logger.info("promo updated from PromoPointsView")

        return self.partial_update(request, *args, **kwargs)