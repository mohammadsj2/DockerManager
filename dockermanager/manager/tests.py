from django.test import TestCase
from django.test import Client
from manager.models import App, AppEnvVar
from rest_framework.test import APIClient


class TestSet(TestCase):
    def setUp(self):
        app1 = App.objects.create(name="my-app", image_url="hub.hamdocker.ir/nginx:1.21", command="echo hello")
        app2 = App.objects.create(name="my app2", image_url="hub.hamdocker.ir/nginx", command="echo hello2")
        AppEnvVar.objects.create(key="k1", val="v1", app=app1)
        AppEnvVar.objects.create(key="k2", val="v2", app=app1)

        AppEnvVar.objects.create(key="k1", val="v1", app=app2)
        AppEnvVar.objects.create(key="k3", val="v1", app=app2)

    def test_apps_list(self):
        c = APIClient()
        response = c.get('/apps/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         b'[{"name":"my-app","image":"hub.hamdocker.ir/nginx:1.21","envs":{"k1":"v1","k2":"v2"},'
                         b'"command":"echo hello"},'
                         b'{"name":"my app2","image":"hub.hamdocker.ir/nginx","envs":{"k1":"v1","k3":"v1"},'
                         b'"command":"echo hello2"}]')

    def test_get_app(self):
        c = APIClient()
        response = c.get('/apps/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         b'{"name":"my-app","image":"hub.hamdocker.ir/nginx:1.21","envs":{"k1":"v1","k2":"v2"},'
                         b'"command":"echo hello"}')

    def test_del_app(self):
        c = APIClient()
        response = c.post('/apps/1/delete/')
        response = c.get('/apps/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         b'[{"name":"my app2","image":"hub.hamdocker.ir/nginx","envs":{"k1":"v1","k3":"v1"},'
                         b'"command":"echo hello2"}]')

    def test_create_update_app(self):
        c = APIClient()
        c.post('/apps/create/', {'name': 'new app', 'image': 'new.ir/nginx:1.21',
                                 'envs': {'k22': 'val22', 'k33': 'val33'}, 'command': 'echo new'}, format='json')
        response = c.get('/apps/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         b'{"name":"new app","image":"new.ir/nginx:1.21","envs":{"k22":"val22","k33":"val33"},'
                         b'"command":"echo new"}')
        c.post('/apps/3/edit/', {'name': 'new app', 'image': 'new.ir/nginx:1.21',
                                 'envs': {'k2222': 'val22', 'k3322': 'val32'}, 'command': 'echo new'}, format='json')
        response = c.get('/apps/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         b'{"name":"new app","image":"new.ir/nginx:1.21","envs":{"k2222":"val22","k3322":"val32"},'
                         b'"command":"echo new"}')

    def test_container(self):
        c = APIClient()
        app = App.objects.create(name="new", image_url="hub.hamdocker.ir/nginx:1.21", command="sleep 1000")
        AppEnvVar.objects.create(key="key1", val="val1", app=app)
        AppEnvVar.objects.create(key="key2", val="val2", app=app)
        c.post('/apps/3/containers/create/')
        c.post('/apps/3/containers/create/')
        response = c.get('/apps/3/containers/')
        print(response.content)
        c.post('/apps/3/delete/')

    def test_container2(self):
        c = APIClient()
        app = App.objects.create(name="new", image_url="ubuntu", command="echo hello")
        AppEnvVar.objects.create(key="key1", val="val1", app=app)
        AppEnvVar.objects.create(key="key2", val="val2", app=app)
        c.post('/apps/3/containers/create/')
        c.post('/apps/3/containers/create/')
        response = c.get('/apps/3/containers/')
        print(response.content)
        c.post('/apps/3/delete/')
