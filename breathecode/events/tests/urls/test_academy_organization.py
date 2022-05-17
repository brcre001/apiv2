import re
from breathecode.events.caches import EventCache
from django.urls.base import reverse_lazy
from datetime import datetime
from breathecode.utils import Cache
from unittest.mock import patch
from ..mixins.new_events_tests_case import EventTestCase
from django.utils import timezone
from rest_framework import status


def serialize_get_data(self, model, data={}):
    info = {
        'id': model.organization.id,
        'eventbrite_id': model.organization.eventbrite_id,
        'eventbrite_key': model.organization.eventbrite_key,
        'name': model.organization.name,
        'sync_status': model.organization.sync_status,
        'sync_desc': model.organization.sync_desc,
        **data
    }
    return info


# def serialize_post_data():

# def serialize_put_data():


class AcademyOrganizationTestSuite(EventTestCase):
    def test_get_academy_organization_no_auth(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        response = self.client.get(url)
        json = response.json()
        expected = {'detail': 'Authentication credentials were not provided.', 'status_code': 401}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_academy_organization_no_organization(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        capability='read_organization',
                                        role='potato',
                                        cohort=1)

        response = self.client.get(url)
        json = response.json()
        expected = {'detail': 'org-not-found', 'status_code': 400}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_academy_organization_with_organization(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        organization=1,
                                        capability='read_organization',
                                        role='potato',
                                        cohort=1)

        response = self.client.get(url)
        json = response.json()

        del json['created_at']
        del json['updated_at']

        expected = serialize_get_data(self, model)

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_academy_organization_no_auth(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {}
        response = self.client.post(url, data)
        json = response.json()
        expected = {'detail': 'Authentication credentials were not provided.', 'status_code': 401}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_academy_organization_without_name(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {}
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        capability='crud_organization',
                                        role='potato',
                                        cohort=1)

        response = self.client.post(url, data)
        json = response.json()

        expected = {'name': ['This field is required.']}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_academy_organization_without_academy(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {}
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        capability='crud_organization',
                                        role='potato',
                                        cohort=1)

        response = self.client.post(url, data)
        json = response.json()
        print(json)

        expected = {'name': ['This field is required.']}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_academy_organization_without_existing_organization(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {'name': '4Geeks'}
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        capability='crud_organization',
                                        role='potato',
                                        cohort=1)

        response = self.client.post(url, data)
        json = response.json()
        print(json)

        # del json['created_at']
        # del json['updated_at']

        expected = {
            'id': 1,
            'eventbrite_id': '',
            'eventbrite_key': None,
            'name': '4Geeks',
            'sync_status': 'PENDING',
            'sync_desc': None,
            'academy': 1
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_academy_organization_with_existing_organization(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {}
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        organization=1,
                                        capability='crud_organization',
                                        role='potato',
                                        cohort=1)

        response = self.client.post(url, data)
        json = response.json()
        expected = {'detail': 'already-created', 'status_code': 400}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_academy_organization_with_incorrect_data(self):

        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {
            'eventbrite_id': '',
            'eventbrite_key': '',
            'name': '',
            'sync_status': 'PENDING',
            'sync_desc': '',
        }
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        capability='crud_organization',
                                        role='potato',
                                        cohort=1)

        response = self.client.post(url, data)
        json = response.json()
        expected = {
            'eventbrite_id': ['Not a valid string.'],
            'eventbrite_key': ['Not a valid string.'],
            'name': ['Not a valid string.'],
            'sync_status': ['"[\'PENDING\']" is not a valid choice.'],
            'sync_desc': ['Not a valid string.']
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_academy_organization_with_no_auth(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {}
        response = self.client.put(url, data)
        json = response.json()
        expected = {'detail': 'Authentication credentials were not provided.', 'status_code': 401}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_academy_organization_without_existing_organization(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {}
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        capability='crud_organization',
                                        role='potato',
                                        cohort=1)

        response = self.client.put(url, data)
        json = response.json()

        expected = {'detail': 'org-not-found', 'status_code': 400}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_academy_organization_with_existing_organization(self):
        self.headers(academy=1)

        url = reverse_lazy('events:academy_organization')
        data = {'eventbrite_id': 'cwRtiODa'}
        model = self.bc.database.create(authenticate=True,
                                        profile_academy=1,
                                        capability='crud_organization',
                                        role='potato',
                                        organization=1,
                                        cohort=1)

        response = self.client.put(url, data)
        json = response.json()
        print(json)

        del json['created_at']
        del json['updated_at']

        expected = {
            'id': model['organization'].id,
            'eventbrite_id': model['organization'].eventbrite_id,
            'eventbrite_key': model['organization'].eventbrite_key,
            'name': model['organization'].name,
            'sync_status': model['organization'].sync_status,
            'sync_desc': model['organization'].sync_desc,
            'academy': model['organization'].academy
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
