from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from api_rest.models import AppException, Agent, ErrorLog


class ViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            password="t3st3us3rp4ssw0rd",
            username='TestUser'
        )

        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.create_objects()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def create_objects(self):
        e1 = AppException.objects.create(title="NullPointerException")
        a1 = Agent.objects.create(address="http://127.0.0.1:8000")

        ErrorLog.objects.create(description="in method save() at line 5",
                                level="ERROR", environment="DEVELOPMENT",
                                agent=a1, user=self.user,
                                exception=e1)

        e2 = AppException.objects.create(title="BadRequestException")
        a2 = Agent.objects.create(address="http://www.prod.com.br")

        ErrorLog.objects.create(description="in method update() at line 3",
                                level="WARNING", environment="PRODUCTION",
                                agent=a2, user=self.user,
                                exception=e2)

        print("Created")

    def test_should_retrieve_all_log_list(self):
        response = self.client.get('/api/logs/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_should_retrieve_logs_filtered_by_environment(self):
        response = self.client.get('/api/logs/?environment=PRODUCTION')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['environment'], 'PRODUCTION')

    def test_should_retrieve_logs_filtered_by_level(self):
        response = self.client.get('/api/logs/?level=ERROR')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['level'], 'ERROR')

    def test_should_retrieve_logs_filtered_by_description(self):
        response = self.client.get('/api/logs/?description=update')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['description'], 'in method update() at line 3')

    def test_should_retrieve_logs_filtered_by_agent(self):
        response = self.client.get('/api/logs/?agent=2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['agent']['address'], 'http://www.prod.com.br')

    def test_should_create_log(self):
        log = {
            'agent': 1,
            'environment': "HOMOLOGATION",
            'level': "ERROR",
            'description': 'ErrorDescription',
            'exception': 1
        }

        response = self.client.post('/api/logs/', data=log, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], log['description'])

    def test_should_retrieve_log_by_id(self):
        response = self.client.get('/api/logs/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_should_remove_log_by_id(self):
        response = self.client.delete('/api/logs/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        get_response = self.client.get('/api/logs/1/')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_not_create_log_when_environment_is_invalid(self):
        log = {
            'agent': 1,
            'environment': "INVALID_ENVIRONMENT",
            'level': "ERROR",
            'description': 'ErrorDescription',
            'exception': 1
        }

        response = self.client.post('/api/logs/', data=log, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['environment'][0], "\"INVALID_ENVIRONMENT\" não é um escolha válido.")

    def test_should_not_create_log_when_level_is_invalid(self):
        log = {
            'agent': 1,
            'environment': "DEVELOPMENT",
            'level': "INVALID_LEVEL",
            'description': 'ErrorDescription',
            'exception': 1
        }

        response = self.client.post('/api/logs/', data=log, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['level'][0], "\"INVALID_LEVEL\" não é um escolha válido.")

    def test_should_retrieve_logs_filtered_by_exception(self):
        response = self.client.get('/api/logs/?exception=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['exception']['id'], 1)

    def test_should_retrieve_summaries(self):
        response = self.client.get('/api/summaries/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['exception']['id'], 1)
        self.assertEqual(response.data['results'][0]['events'], 1)

    def test_should_retrieve_summaries_filtered_by_exception(self):
        response = self.client.get('/api/summaries/?exception=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['exception']['id'], 1)
        self.assertEqual(response.data['results'][0]['events'], 1)
