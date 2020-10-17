from rest_framework import serializers
from core.models import Promo,User

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo 
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

    def validate_promo(self, instance):
        qs = Promo.objects.filter(promo__iexact=instance)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This promo already exist")
        return instance

    def validate_promo_amount(self, instance):
        if instance <= 0:
            raise serializers.ValidationError("invalid promo amount")
        return instance

    def validate_user(self, instance):
        user = User.objects.get(username=instance)
        if user.is_staff:
            raise serializers.ValidationError('promo for users only')
        return instance

class PromoPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo 
        fields = (
            'id', '_type',
            'promo', 'amount'
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)

    def validate_username(self, instance):
        
        qs = User.objects.filter(username__iexact=instance) 
        if qs.exists():
            raise serializers.ValidationError("This username already exist")
        return instance
