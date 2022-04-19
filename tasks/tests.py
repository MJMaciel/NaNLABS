from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TrelloTestCase(APITestCase):
    task_url = reverse('task-list')

    def test_task(self):
        data = {
            'type': 'task',
            'title': 'task title',
            'category': 'maintenance'
        }
        response = self.client.post(self.task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_request_task(self):
        data = {
            'type': 'task',
            'title': 'task title',
        }
        response = self.client.post(self.task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bug(self):
        data = {
            'type': 'bug',
            'description': 'short description',
        }
        response = self.client.post(self.task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_request_bug(self):
        data = {
            'type': 'bug',
        }
        response = self.client.post(self.task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_issue(self):
        data = {
            'type': 'issue',
            'title': 'issue title',
            'description': 'issue description',
        }
        response = self.client.post(self.task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_request_issue(self):
        data = {
            'type': 'issue',
            'description': 'issue description',
        }
        response = self.client.post(self.task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)