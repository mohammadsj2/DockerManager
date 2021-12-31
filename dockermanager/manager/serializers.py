from rest_framework import serializers
from manager.models import App, AppEnvVar, Container, ContainerEnvVar
import docker


class AppSerializerHelper:
    def __init__(self, app: App):
        self.name = app.name
        self.image = app.image_url
        self.envs = {}
        self.command = app.command
        env_vars = AppEnvVar.objects.filter(app=app).all()
        for envVar in env_vars:
            self.envs[envVar.key] = envVar.val


class AppFullSerializer(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.URLField()
    envs = serializers.DictField(child=serializers.CharField())
    command = serializers.CharField()


class ContainerSerializerHelper:
    def __init__(self, container: Container):
        self.name = container.name
        self.image = container.image_url
        self.envs = {}
        self.command = container.command
        self.start_time = container.start_time

        self.status = 'Finished'
        client = docker.from_env()
        container_objs = client.containers.list(all=True, filters={'id': container.container_id})
        if len(container_objs) > 0:
            container_objs[0].reload()
            self.status = container_objs[0].status

        env_vars = ContainerEnvVar.objects.filter(container=container).all()
        for envVar in env_vars:
            self.envs[envVar.key] = envVar.val


class ContainerFullSerializer(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.URLField()
    envs = serializers.DictField(child=serializers.CharField())
    command = serializers.CharField()
    start_time = serializers.DateTimeField()
    status = serializers.CharField()
