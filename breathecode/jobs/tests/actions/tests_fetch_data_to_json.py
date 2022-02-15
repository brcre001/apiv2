"""
Tasks tests
"""
from unittest.mock import patch, call, MagicMock
from ...actions import fetch_data_to_json
from ..mixins import JobsTestCase
from breathecode.tests.mocks.django_contrib import DJANGO_CONTRIB_PATH, apply_django_contrib_messages_mock
from breathecode.tests.mocks import (
    REQUESTS_PATH,
    apply_requests_get_mock,
    apply_requests_post_mock,
)

DATA = {
    'status':
    'ok',
    'count':
    3,
    'total':
    3,
    'jobs': [{
        'priority': 2,
        'tags': [],
        'version': '2f9f2a5-master',
        'state': 'finished',
        'spider_type': 'manual',
        'spider': 'indeed',
        'spider_args': {
            'job': 'front end',
            'loc': 'remote'
        },
        'close_reason': 'finished',
        'elapsed': 609370879,
        'logs': 74,
        'id': '570286/2/72',
        'started_time': '2022-01-02T22:56:02',
        'updated_time': '2022-01-02T23:53:52',
        'items_scraped': 227,
        'errors_count': 0,
        'responses_received': 555
    }, {
        'priority': 2,
        'tags': [],
        'version': '2f9f2a5-master',
        'state': 'finished',
        'spider_type': 'manual',
        'spider': 'getonboard',
        'spider_args': {
            'job': 'go',
            'loc': 'remote'
        },
        'close_reason': 'finished',
        'elapsed': 646146617,
        'logs': 18,
        'id': '570286/3/35',
        'started_time': '2022-01-02T13:40:20',
        'updated_time': '2022-01-02T13:40:57',
        'items_scraped': 6,
        'errors_count': 0,
        'responses_received': 2
    }, {
        'priority': 2,
        'tags': [],
        'version': '2f9f2a5-master',
        'state': 'finished',
        'spider_type': 'manual',
        'spider': 'getonboard',
        'spider_args': {
            'job': 'web developer',
            'loc': 'remote'
        },
        'close_reason': 'finished',
        'elapsed': 647281256,
        'logs': 25,
        'id': '570286/3/34',
        'started_time': '2022-01-02T13:15:17',
        'updated_time': '2022-01-02T13:22:03',
        'items_scraped': 3,
        'errors_count': 2,
        'responses_received': 0
    }]
}

JOBS = [{
    'Searched_job': 'junior web developer',
    'Job_title': 'Desarrollador Full-Stack',
    'Location': 'Santiago (temporarily remote)',
    'Company_name': 'Centry',
    'Post_date': 'January 19, 2022',
    'Extract_date': '2022-01-30',
    'Job_description': '',
    'Salary': '$1800 - 2100 USD/month',
    'Tags': ['api', 'back-end', 'full-stack', 'git', 'java', 'mvc', 'python', 'ruby'],
    'Apply_to':
    'https://www.getonbrd.com/jobs/programming/desarrollador-full-stack-developer-centry-santiago',
    '_type': 'dict'
}, {
    'Searched_job':
    'junior web developer',
    'Job_title':
    'Desarrollador Full-Stack Python/React',
    'Location':
    'Remote',
    'Company_name':
    'Alluxi',
    'Post_date':
    'January 14, 2022',
    'Extract_date':
    '2022-01-30',
    'Job_description':
    'Al menos 1 año de experiencia trabajando con Python y Django Al menos 1 año de experiencia trabajando con React.js Experiencia desarrollando APIs REST Ingles Conversacional Buscamos un desarrollador responsable, autodidacta, proactivo, eficiente y organizado.',
    'Salary':
    '$1800 - 2000 USD/month',
    'Tags':
    ['api', 'back-end', 'django', 'english', 'front-end', 'full-stack', 'javascript', 'python', 'react'],
    'Apply_to':
    'https://www.getonbrd.com/jobs/programming/desarrollodor-fullstack-python-react-alluxi-remote',
    '_type':
    'dict'
}, {
    'Searched_job':
    'junior web developer',
    'Job_title':
    'Full-Stack Developer',
    'Location':
    'Santiago',
    'Company_name':
    'AAXIS Commerce',
    'Post_date':
    'January 17, 2022',
    'Extract_date':
    '2022-01-30',
    'Job_description':
    'Four-year degree in any computer science-related field or equivalent experience. At least 3-year solid front-end developer as well as back-end full stack developer. Relevant experience working with PHP/Symfony (if it is in Magento or Oro Commerce, even better). Familiar with responsive/adaptive design and mobile development best practices. Web and mobile development, familiar with front+back end developing and data interaction.  Experience with Express, Redis. and Node.js, mainframe (React, Angular, Knockout) preferred for React.',
    'Salary':
    'Not supplied',
    'Tags': [
        'angularjs', 'back-end', 'express', 'front-end', 'full-stack', 'javascript', 'magento',
        'mobile development', 'node.js', 'php', 'react', 'redis', 'responsive', 'symfony', 'ui design'
    ],
    'Apply_to':
    'https://www.getonbrd.com/jobs/programming/full-stack-developer-aaxis-commerce-santiago-3c8e',
    '_type':
    'dict'
}, {
    'Searched_job': 'junior web developer',
    'Job_title': 'Pentester Cybersecurity',
    'Location': 'Remote (Chile)',
    'Company_name': 'Rule 1 Ventures',
    'Post_date': 'November 05, 2021',
    'Extract_date': '2022-01-30',
    'Job_description': 'Vuln exploitation Security reports',
    'Salary': 'Not supplied',
    'Tags': ['back-end', 'cybersecurity', 'english', 'pentesting', 'python'],
    'Apply_to': 'https://www.getonbrd.com/jobs/cybersecurity/security-engineer-rule-1-ventures-remote',
    '_type': 'dict'
}, {
    'Searched_job': 'junior web developer',
    'Job_title': 'Pentester Cybersecurity',
    'Location': 'Remote (Chile, Venezuela)',
    'Company_name': 'Rule 1 Ventures',
    'Post_date': 'November 05, 2021',
    'Extract_date': '2022-01-30',
    'Job_description': 'Vuln exploitation Security reports',
    'Salary': 'Not supplied',
    'Tags': ['back-end', 'cybersecurity', 'english', 'pentesting', 'python'],
    'Apply_to': 'https://www.getonbrd.com/jobs/cybersecurity/security-engineer-rule-1-ventures-remote',
    '_type': 'dict'
}, {
    'Searched_job': 'junior web developer',
    'Job_title': 'Front-end Developer',
    'Location': 'Lima',
    'Company_name': 'ID Business Intelligence',
    'Post_date': 'January 24, 2022',
    'Extract_date': '2022-01-30',
    'Job_description':
    'Manejo de Git Flow. (~°-°)~ Dominar a profundidad CSS y JS (mínimo 1 año) Experiencia con React Experiencia consumiendo Web Service (Rest) Preocuparse por entregar productos de calidad.',
    'Salary': 'Not supplied',
    'Tags': ['api', 'css', 'front-end', 'git', 'javascript', 'react'],
    'Apply_to': 'https://www.getonbrd.com/jobs/programming/fronted-developer-id-business-intelligence-remote',
    '_type': 'dict'
}, {
    'Searched_job':
    'junior web developer',
    'Job_title':
    'Junior Web Developer',
    'Location':
    None,
    'Company_name':
    'Reign',
    'Post_date':
    'January 29, 2022',
    'Extract_date':
    '2022-01-30',
    'Job_description':
    '',
    'Salary':
    'Not supplied',
    'Tags': [
        'angularjs', 'api', 'back-end', 'ci/cd', 'css', 'docker', 'front-end', 'html5', 'javascript', 'json',
        'mongodb', 'node.js', 'nosql', 'postgresql', 'react', 'responsive', 'ui design', 'virtualization'
    ],
    'Apply_to':
    'https://www.getonbrd.com/jobs/programming/junior-web-developer-reign-remote',
    '_type':
    'dict'
}]

DATA2 = [{'status': 'ok', 'data': [45, 12]}]
DATA3 = [{'status': 'ok', 'data': [1, 2]}]

DATA4 = [{'status_code': 401}]


class ActionFetchDataToJsonTestCase(JobsTestCase):
    @patch(DJANGO_CONTRIB_PATH['messages'], apply_django_contrib_messages_mock())
    @patch('django.contrib.messages.add_message', MagicMock())
    @patch('logging.Logger.error', MagicMock())
    def test_fetch_data_to_json__without_spider(self):
        from breathecode.jobs.actions import fetch_data_to_json
        from logging import Logger
        try:
            fetch_data_to_json(None, DATA)
        except Exception as e:
            self.assertEquals(str(e), ('without-spider'))
            self.assertEqual(Logger.error.call_args_list, [
                call('First you must specify a spider (fetch_data_to_json)'),
                call('Status 400 - without-spider')
            ])

    @patch(DJANGO_CONTRIB_PATH['messages'], apply_django_contrib_messages_mock())
    @patch('django.contrib.messages.add_message', MagicMock())
    @patch('logging.Logger.error', MagicMock())
    def test_fetch_data_to_json__without_data(self):
        from breathecode.jobs.actions import fetch_data_to_json
        from logging import Logger

        try:
            model = self.generate_models(spider=True)

            fetch_data_to_json(model.spider, None)
        except Exception as e:
            self.assertEquals(str(e), ('no-return-json-data'))
            self.assertEqual(Logger.error.call_args_list, [
                call('I did not receive results from the API (fetch_data_to_json)'),
                call('Status 400 - no-return-json-data')
            ])

    @patch(REQUESTS_PATH['get'],
           apply_requests_get_mock([
               (200, 'https://storage.scrapinghub.com/items/570286/3/35?apikey=1234567&format=json', DATA2),
               (200, 'https://storage.scrapinghub.com/items/570286/3/34?apikey=1234567&format=json', DATA3)
           ]))
    def test_fetch_data__with_two_spider(self):
        import requests

        spider = {'zyte_spider_number': 3, 'zyte_job_number': 0}
        zyte_project = {'zyte_api_key': 1234567}
        platform = {'name': 'getonboard'}

        model = self.generate_models(spider=spider, zyte_project=zyte_project, platform=platform)

        result = fetch_data_to_json(model.spider, DATA)

        self.assertEqual(result, [{
            'status': 'ok',
            'platform_name': model.platform.name,
            'num_spider': 3,
            'num_job': 35,
            'jobs': DATA2
        }, {
            'status': 'ok',
            'platform_name': model.platform.name,
            'num_spider': 3,
            'num_job': 34,
            'jobs': DATA3
        }])
        self.assertEqual(requests.get.call_args_list, [
            call('https://storage.scrapinghub.com/items/570286/3/35?apikey=1234567&format=json'),
            call('https://storage.scrapinghub.com/items/570286/3/34?apikey=1234567&format=json')
        ])
