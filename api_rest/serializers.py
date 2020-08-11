from djoser.serializers import UserSerializer
from rest_framework import serializers

from api_rest.models import Agent, AppException, ErrorLog


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"


class AppExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppException
        fields = ['id', 'title']


class ErrorLogSerializerSummary(serializers.ModelSerializer):
    events = serializers.IntegerField()
    agent = AgentSerializer()
    exception = AppExceptionSerializer()

    class Meta:
        model = ErrorLog
        fields = ['level', 'agent', 'environment', 'exception', 'events']

    def to_representation(self, instance):
        exception = AppException(id=instance.pop('exception__id'),
                                 title=instance.pop('exception__title'))

        agent = Agent(id = instance.pop("agent__id"),
                      address=instance.pop("agent__address"))

        instance['exception'] = exception
        instance['agent'] = agent

        return super().to_representation(instance)


class ErrorLogSerializerList(serializers.ModelSerializer):
    agent = AgentSerializer()
    exception = AppException()
    user = UserSerializer()

    class Meta:
        model = ErrorLog
        fields = "__all__"


class ErrorLogSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = ['description', 'agent', 'level', 'environment', 'exception']

