import docker
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class App(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200)
    command = models.URLField(max_length=400)


class Container(models.Model):
    app = models.ForeignKey(App, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200)
    command = models.URLField(max_length=400)
    start_time = models.DateTimeField(auto_now=True)
    container_id = models.CharField(max_length=200)


@receiver(pre_delete, sender=Container)
def pre_delete_container(sender, **kwargs):
    try:
        container = kwargs['instance']
        client = docker.from_env()
        container_obj = client.containers.list(filters={'id': container.container_id})
        if len(container_obj) != 0:
            container_obj[0].kill()
    except Exception as e:
        print(e)
        pass


class EnvVar(models.Model):
    key = models.CharField(max_length=100)
    val = models.CharField(max_length=100)


class AppEnvVar(EnvVar):
    app = models.ForeignKey(App, on_delete=CASCADE)


class ContainerEnvVar(EnvVar):
    container = models.ForeignKey(Container, on_delete=CASCADE)
