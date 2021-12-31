from rest_framework import generics, permissions
from rest_framework.response import Response

from manager.models import App, AppEnvVar, ContainerEnvVar, Container
from manager.serializers import AppSerializerHelper, AppFullSerializer, ContainerSerializerHelper, \
    ContainerFullSerializer
import docker


class AppList(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        try:
            apps = App.objects.all()
            apps = [AppSerializerHelper(app) for app in apps]
            result = AppFullSerializer(apps, many=True).data
            return Response(result)
        except Exception as e:
            print(e)
            return Response('Error')


class CreateApp(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        try:
            necessary_fields = ['name', 'image', 'command', 'envs']
            if not all([field in request.data for field in necessary_fields]):
                return Response('You have to get all the necessary fields. Necessary fields: ' + str(necessary_fields))

            app = App(name=request.data['name'], image_url=request.data['image'], command=request.data['command'])
            app.save()
            envs = request.data['envs']
            for key in envs:
                env_var = AppEnvVar(key=key, val=envs[key], app=app)
                env_var.save()
            return Response()
        except Exception as e:
            print(e)
            return Response('Error')


class GetApp(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, app_id):
        try:
            app = App.objects.filter(id=app_id).first()
            if app is None:
                return Response('There is no app with this id')
            app = AppSerializerHelper(app)
            result = AppFullSerializer(app).data
            return Response(result)
        except Exception as e:
            print(e)
            return Response('Error')


class DeleteApp(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request, app_id):
        try:
            app = App.objects.filter(id=app_id).first()
            if app is None:
                return Response('There is no app with this id')
            app.delete()
            return Response()
        except Exception as e:
            print(e)
            return Response('Error')


class EditApp(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, app_id):
        try:
            necessary_fields = ['name', 'image', 'command', 'envs']
            if not all([field in request.data for field in necessary_fields]):
                return Response('You have to get all the necessary fields. Necessary fields: ' + str(necessary_fields))

            app = App.objects.filter(id=app_id).first()
            if app is None:
                return Response('There is no app with this id')
            AppEnvVar.objects.filter(app=app).delete()
            app.name = request.data['name']
            app.image_url = request.data['image']
            app.command = request.data['command']
            app.save()
            envs = request.data['envs']
            for key in envs:
                env_var = AppEnvVar(key=key, val=envs[key], app=app)
                env_var.save()
            return Response()
        except Exception as e:
            print(e)
            return Response('Error')


class ContainerList(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, app_id):
        try:
            app = App.objects.filter(id=app_id).first()
            if app is None:
                return Response('There is no app with this id')
            containers = Container.objects.filter(app=app).all()
            containers = [ContainerSerializerHelper(container) for container in containers]
            result = ContainerFullSerializer(containers, many=True).data
            return Response(result)
        except Exception as e:
            print(e)
            return Response('Error')


class CreateContainer(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request, app_id):
        try:
            original_app = App.objects.filter(id=app_id).first()
            if original_app is None:
                return Response('There is no app with this id')
            app = AppSerializerHelper(original_app)
            client = docker.from_env()
            container_obj = client.containers.run(image=app.image, environment=app.envs, command=app.command,
                                                  detach=True)
            container_obj.reload()
            container = Container(name=app.name, image_url=app.image, command=app.command, app=original_app,
                                  container_id=container_obj.id)
            container.save()
            for key in app.envs:
                env_var = ContainerEnvVar(key=key, val=app.envs[key], container=container)
                env_var.save()
            return Response()
        except Exception as e:
            print(e)
            return Response('Error')
