from rest_framework import serializers

from .models import SocialDashboardData



class SocialDashboardDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialDashboardData
        exclude = ('id','postid','modified_at')