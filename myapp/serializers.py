from rest_framework import serializers
from .models import PlannerTask

class PlannerTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannerTask
        fields = '__all__'
