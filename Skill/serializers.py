from rest_framework import serializers
from .models import *

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'



from rest_framework import serializers
from .models import Trade, Skill

class TradeSerializer(serializers.ModelSerializer):
    initiator_skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), required=True)
    desired_skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), required=True)
    responder_skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), required=False)

    class Meta:
        model = Trade
        fields = ['id', 'initiator', 'responder', 'initiator_skills', 'responder_skills', 'desired_skills', 'status', 'initiator_terms', 'responder_terms', 'created_at', 'completed_at', 'title', 'description']
        read_only_fields = ['initiator']

    def create(self, validated_data):
        initiator_skills = validated_data.pop('initiator_skills')
        desired_skills = validated_data.pop('desired_skills')
        responder_skills = validated_data.pop('responder_skills', [])

        trade = Trade.objects.create(**validated_data)

        for skill in initiator_skills:
            trade.initiator_skills.add(skill)

        for skill in desired_skills:
            trade.desired_skills.add(skill)

        for skill in responder_skills:
            trade.responder_skills.add(skill)

        return trade

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source='reviewer.username')
    reviewee = serializers.ReadOnlyField(source='reviewee.username')

    class Meta:
        model = Review
        fields = '__all__'



class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = '__all__'
        read_only_fields = ['id', 'applied_at', 'invited_at', 'accepted_at', 'rejected_at']









class QueueResponseSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'decline'])
    responder_terms = serializers.CharField(required=False, allow_blank=True)
    responder_skills = serializers.ListField(child=serializers.IntegerField(), required=False)










class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'