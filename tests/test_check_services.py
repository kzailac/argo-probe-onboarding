import datetime
import unittest
from unittest import mock

from argo_probe_onboarding.catalog import CatalogAPI, CriticalException
from requests.exceptions import RequestException

catalog_data = [
    {
        'erp_gla_geographical_availability': 'Europe',
        'erp_cli_category': [
            {
                'supercategory':
                    'https://agora.ni4os.eu/api/v2/public/supercategor'
                    'ies/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/',
                'href':
                    'https://agora.ni4os.eu/api/v2/public/'
                    'categories/1xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/',
                'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1',
                'name': 'Data'
            }, {
                'supercategory':
                    'https://agora.ni4os.eu/api/v2/public/'
                    'supercategories/xxxxxxxx-xxxx-xxxx-xxxx-'
                    'xxxxxxxxxxx2/',
                'href':
                    'https://agora.ni4os.eu/api/v2/public/categories/'
                    'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx3/',
                'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx3',
                'name': 'Communication'
            }
        ],
        'erp_cli_target_users': [{
            'description':
                'A research group is a group of researchers working '
                'together on a particular issue or topic.',
            'href':
                'https://agora.ni4os.eu/api/v2/public/target-users/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx4/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx4',
            'user': 'Research Groups'
        }, {
            'description':
                'Someone in an organization whose job is to manage a '
                'research initiative aiming to the development of new '
                'scientific results, products or ideas.',
            'href':
                'https://agora.ni4os.eu/api/v2/public/target-users/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx5/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx5',
            'user': 'Research Managers'
        }],
        'erp_coi_organisation': 'Ministry of Funny Walks',
        'erp_cli_scientific_subdomain': [{
            'domain':
                'https://agora.ni4os.eu/api/v2/public/domains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx6/',
            'href':
                'https://agora.ni4os.eu/api/v2/public/subdomains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx7/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx7',
            'name': 'Electrical, Electronic & Information Engineering'
        }, {
            'domain':
                'https://agora.ni4os.eu/api/v2/public/domains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx8/',
            'href':
                'https://agora.ni4os.eu/api/v2/public/subdomains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx9/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx9',
            'name': 'Economics & Business'
        }],
        'erp_mti_last_update': None,
        'erp_bai_webpage': 'https://service1.example.com/',
        'erp_bai_abbreviation': '',
        'erp_mgi_privacy_policy': None,
        'erp_bai_name': 'Some service',
        'published_at': '2021-02-15T22:22:13',
        'erp_mgi_sla_specification': '',
        'erp_mri_multimedia': None,
        'erp_mti_technology_readiness_level': {
            'description':
                'Actual system proven in operational environment '
                '(competitive manufacturing in the case of key '
                'enabling technologies; or in space)',
            'href':
                'https://agora.ni4os.eu/api/v2/public/trls/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx10/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx10',
            'name': 'TRL9'
        },
        'erp_mti_changelog': None,
        'erp_mti_version': None,
        'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11',
        'erp_mri_logo': 'https://service.example.com/logo.png',
        'erp_bai_providers_public': [{
            'epp_bai_name': 'Providing provider',
            'href':
                'https://agora.ni4os.eu/api/v2/public/providers/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx12/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx12',
            'epp_bai_id': 'pr-pr'
        }],
        'erp_mti_open_source_technologies': 'Linux\nApache\nPostgreSQL',
        'erp_gla_language': 'en',
        'erp_coi_first_name': 'Meh',
        'erp_coi_helpdesk_email': "meh@example.com",
        'erp_mri_use_cases': None,
        'erp_mgi_helpdesk_webpage':
            'https://catalogue.ni4os.eu/?_=/helpdesk/'
            'Repositories/somethingsomething',
        'erp_cli_scientific_domain': [{
            'href':
                'https://agora.ni4os.eu/api/v2/public/domains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx13/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx13',
            'name': 'Agricultural Sciences'
        }],
        'erp_cli_subcategory': [{
            'category':
                'https://agora.ni4os.eu/api/v2/public/categories/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx14/',
            'href':
                'https://agora.ni4os.eu/api/v2/public/subcategories/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx13/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx13',
            'name': 'Discovery'
        }],
        'erp_ati_funding_body': [],
        'erp_coi_phone': '+111111111',
        'erp_rli_geographic_location': 'Greece (GR)',
        'erp_fni_payment_model': None,
        'erp_mgi_maintenance': None,
        'erp_coi_email': 'info@example.com',
        'erp_mgi_training_information':
            'https://training.ni4os.eu/course/view.php?id=10',
        'erp_coi_security_contact_email': 'info@example.com',
        'updated_at': '2022-04-22T13:43:55',
        'erp_dei_required_resources_public': [],
        'erp_cli_access_mode': [{
            'description':
                'Users can freely access the Resource provided, '
                'registration may be needed.',
            'href':
                'https://agora.ni4os.eu/api/v2/public/access-modes/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx14/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx14',
            'name': 'Free'
        }],
        'erp_aoi_order': None,
        'erp_mgi_status_monitoring':
            'https://argo.ni4os.eu/ni4os/report-status/Critical/SITES/'
            'RCUB/eu.ni4os.repo.publication/meh.example.com',
        'erp_cli_access_type': [{
            'description':
                'The Resource is delivered through a virtual '
                'infrastructure that the use may access virtually '
                'through the web or an intranet.',
            'href':
                'https://agora.ni4os.eu/api/v2/public/access-types/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx15/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx15',
            'name': 'Virtual'
        }],
        'erp_mri_description':
            '<p>Some long and boring description</p>',
        'erp_mti_life_cycle_status':
            'https://agora.ni4os.eu/api/v2/resource-lifecycle-statuses/'
            'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx16/',
        'erp_bai_organisation_public':
            'https://agora.ni4os.eu/api/v2/public/providers/'
            'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx17/',
        'erp_dei_related_platforms': '',
        'erp_mti_standards': None,
        'created_at': '2021-02-15T22:19:12',
        'erp_aoi_order_type': {
            'description':
                'No ordering procedure necessary to access the '
                'resource but requires user authentication',
            'href':
                'https://agora.ni4os.eu/api/v2/public/order-types/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx18/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx18',
            'name': 'Open Access'
        },
        'erp_cli_tags': 'national repository',
        'erp_coi_position': 'Repository manager',
        'erp_mri_tagline': 'National repository of PhD theses',
        'erp_mgi_user_manual': 'https://example.com/user-manual',
        'erp_bai_id': 'MEH',
        'erp_mti_certifications': None,
        'erp_dei_related_resources_public': [],
        'erp_mgi_terms_of_use': None,
        'erp_ati_grant_project_name': None,
        'erp_ati_funding_program': [],
        'erp_fni_pricing': None,
        'erp_mgi_access_policy': 'https://example.com/contact',
        'erp_coi_last_name': "Bla"
    },
    {
        'erp_gla_geographical_availability': 'Europe',
        'erp_cli_category': [
            {
                'supercategory':
                    'https://agora.ni4os.eu/api/v2/public/supercategor'
                    'ies/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx19/',
                'href':
                    'https://agora.ni4os.eu/api/v2/public/'
                    'categories/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx20/',
                'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx20',
                'name': 'Data'
            }, {
                'supercategory':
                    'https://agora.ni4os.eu/api/v2/public/'
                    'supercategories/xxxxxxxx-xxxx-xxxx-xxxx-'
                    'xxxxxxxxxxx2/',
                'href':
                    'https://agora.ni4os.eu/api/v2/public/categories/'
                    'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx21/',
                'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx21',
                'name': 'Scripts'
            }
        ],
        'erp_cli_target_users': [{
            'description':
                'A research group is a group of researchers working '
                'together on a particular issue or topic.',
            'href':
                'https://agora.ni4os.eu/api/v2/public/target-users/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx4/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx4',
            'user': 'Research Groups'
        }, {
            'description':
                'Someone in an organization whose job is to manage a '
                'research initiative aiming to the development of new '
                'scientific results, products or ideas.',
            'href':
                'https://agora.ni4os.eu/api/v2/public/target-users/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx5/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx5',
            'user': 'Research Managers'
        }],
        'erp_coi_organisation': 'Ministry of Funny Walks',
        'erp_cli_scientific_subdomain': [{
            'domain':
                'https://agora.ni4os.eu/api/v2/public/domains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx6/',
            'href':
                'https://agora.ni4os.eu/api/v2/public/subdomains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx22/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx22',
            'name': 'Mining'
        }, {
            'domain':
                'https://agora.ni4os.eu/api/v2/public/domains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx23/',
            'href':
                'https://agora.ni4os.eu/api/v2/public/subdomains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx23/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx23',
            'name': 'Waste of time'
        }],
        'erp_mti_last_update': None,
        'erp_bai_webpage': 'https://service2.example.com/',
        'erp_bai_abbreviation': '',
        'erp_mgi_privacy_policy': None,
        'erp_bai_name': 'Some other service',
        'published_at': '2021-02-08T11:08:00',
        'erp_mgi_sla_specification': None,
        'erp_mri_multimedia': None,
        'erp_mti_technology_readiness_level': {
            'description':
                'Actual system proven in operational environment '
                '(competitive manufacturing in the case of key '
                'enabling technologies; or in space)',
            'href':
                'https://agora.ni4os.eu/api/v2/public/trls/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx10/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx10',
            'name': 'TRL9'
        },
        'erp_mti_changelog': None,
        'erp_mti_version': None,
        'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx58',
        'erp_mri_logo': 'https://service.sample.com/logo.png',
        'erp_bai_providers_public': [{
            'epp_bai_name': 'THEprovider',
            'href':
                'https://agora.ni4os.eu/api/v2/public/providers/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx24/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx24',
            'epp_bai_id': 'THE'
        }],
        'erp_mti_open_source_technologies': 'Linux\nApache\nPostgreSQL',
        'erp_gla_language': 'en',
        'erp_coi_first_name': 'Meh',
        'erp_coi_helpdesk_email': "meh@sample.com",
        'erp_mri_use_cases': None,
        'erp_mgi_helpdesk_webpage':
            'https://catalogue.ni4os.eu/?_=/helpdesk/'
            'Repositories/and-now-for-something-completely-different',
        'erp_cli_scientific_domain': [{
            'href':
                'https://agora.ni4os.eu/api/v2/public/domains/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx25/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx25',
            'name': 'Animal Sciences'
        }],
        'erp_cli_subcategory': [{
            'category':
                'https://agora.ni4os.eu/api/v2/public/categories/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx26/',
            'href':
                'https://agora.ni4os.eu/api/v2/public/subcategories/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx27/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx27',
            'name': '42'
        }],
        'erp_ati_funding_body': [],
        'erp_coi_phone': '+111111111',
        'erp_rli_geographic_location': 'Croatia (HR)',
        'erp_fni_payment_model': None,
        'erp_mgi_maintenance': None,
        'erp_coi_email': 'info@sample.com',
        'erp_mgi_training_information':
            'https://training.ni4os.eu/course/view.php?id=15',
        'erp_coi_security_contact_email': 'info@sample.com',
        'updated_at': '2022-02-08T14:34:27',
        'erp_dei_required_resources_public': [],
        'erp_cli_access_mode': [{
            'description':
                'Users can freely access the Resource provided, '
                'registration may be needed.',
            'href':
                'https://agora.ni4os.eu/api/v2/public/access-modes/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx28/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx28',
            'name': 'Free'
        }],
        'erp_aoi_order': None,
        'erp_mgi_status_monitoring':
            'https://argo.ni4os.eu/ni4os/report-status/Critical/SITES/'
            'RCUB/eu.ni4os.repo.publication/meh.sample.com',
        'erp_cli_access_type': [{
            'description':
                'The Resource is delivered through a virtual '
                'infrastructure that the use may access virtually '
                'through the web or an intranet.',
            'href':
                'https://agora.ni4os.eu/api/v2/public/access-types/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx15/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx15',
            'name': 'Virtual'
        }],
        'erp_mri_description':
            '<p>Some long and boring description</p>',
        'erp_mti_life_cycle_status':
            'https://agora.ni4os.eu/api/v2/resource-lifecycle-statuses/'
            'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx16/',
        'erp_bai_organisation_public':
            'https://agora.ni4os.eu/api/v2/public/providers/'
            'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx17/',
        'erp_dei_related_platforms': '',
        'erp_mti_standards': None,
        'created_at': '2022-02-08T11:04:44',
        'erp_aoi_order_type': {
            'description':
                'No ordering procedure necessary to access the '
                'resource but requires user authentication',
            'href':
                'https://agora.ni4os.eu/api/v2/public/order-types/'
                'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx18/',
            'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx18',
            'name': 'Open Access'
        },
        'erp_cli_tags': 'national repository',
        'erp_coi_position': 'Repository manager',
        'erp_mri_tagline': 'National repository of PhD theses',
        'erp_mgi_user_manual': 'https://sample.com/users-manual',
        'erp_bai_id': 'MEH',
        'erp_mti_certifications': None,
        'erp_dei_related_resources_public': [],
        'erp_mgi_terms_of_use': None,
        'erp_ati_grant_project_name': None,
        'erp_ati_funding_program': [],
        'erp_fni_pricing': None,
        'erp_mgi_access_policy': 'https://sample.com/contact',
        'erp_coi_last_name': "Blabla"
    }
]


class MockResponse:
    def __init__(self, data, status_code):
        self.status_code = status_code
        self._data = data
        self.ok = str(status_code).startswith("2")

    def raise_for_status(self):
        if not self.ok:
            if self.status_code == 500:
                raise RequestException("500 SERVER ERROR")

            else:
                raise RequestException("418 I am a teapot")

    def json(self):
        return self._data


def mock_get_response(*args, **kwargs):
    if args[0].endswith("users-manual"):
        return MockResponse(data=None, status_code=500)

    elif args[0].endswith("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"):
        return MockResponse(data=catalog_data[0], status_code=200)

    elif args[0].endswith("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx58"):
        return MockResponse(data=catalog_data[1], status_code=200)

    elif args[0].endswith("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx111"):
        return MockResponse(data=None, status_code=418)

    else:
        return MockResponse(data=[], status_code=200)


@mock.patch("requests.get", side_effect=mock_get_response)
class ServiceAPITests(unittest.TestCase):
    def test_check_key_exists(self, mock_request):
        services = CatalogAPI(
            url="https://mock.api.url.com",
            catalog_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11",
            timeout=30
        )
        mock_request.assert_called_once_with(
            "https://mock.api.url.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11",
            timeout=30
        )
        self.assertTrue(services.check_key_exists("erp_mgi_user_manual"))
        self.assertFalse(services.check_key_exists("erp_mgi_user_nanual"))
        self.assertFalse(services.check_key_exists("erp_mgi_privacy_policy"))
        self.assertFalse(services.check_key_exists("erp_mgi_sla_specification"))

    def test_raise_exception_if_no_catalog_response(self, mock_request):
        with self.assertRaises(CriticalException) as context:
            CatalogAPI(
                url="https://mock2.api.url.com",
                catalog_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx111",
                timeout=30
            )
        mock_request.assert_called_once_with(
            "https://mock2.api.url.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx111",
            timeout=30
        )
        self.assertEqual(context.exception.__str__(), "418 I am a teapot")

    def test_check_url_valid(self, mock_request):
        services = CatalogAPI(
            url="https://mock.api.url.com/",
            catalog_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11",
            timeout=30
        )
        self.assertTrue(services.check_url_valid(key="erp_mgi_user_manual"))
        self.assertEqual(mock_request.call_count, 2)
        mock_request.assert_has_calls([
            mock.call(
                "https://mock.api.url.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11",
                timeout=30
            ),
            mock.call("https://example.com/user-manual")
        ], any_order=True)

    def test_check_url_not_valid(self, mock_request):
        services = CatalogAPI(
            url="https://mock.api.url.com/",
            catalog_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx58",
            timeout=30
        )
        with self.assertRaises(CriticalException) as context:
            services.check_url_valid(key="erp_mgi_user_manual")
        self.assertEqual(mock_request.call_count, 2)
        mock_request.assert_has_calls([
            mock.call(
                "https://mock.api.url.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx58",
                timeout=30
            ),
            mock.call("https://sample.com/users-manual")
        ], any_order=True)
        self.assertEqual(
            context.exception.__str__(),
            "URL https://sample.com/users-manual not valid: 500 SERVER ERROR"
        )

    @mock.patch("argo_probe_onboarding.catalog.get_today")
    def test_check_date_age(self, mock_today, _):
        mock_today.return_value = datetime.datetime(2022, 11, 24, 15, 48, 23)
        services = CatalogAPI(
            url="https://mock.api.url.com/",
            catalog_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11",
            timeout=30
        )
        self.assertEqual(
            services.check_date_age(
                key="updated_at", date_format="%Y-%m-%dT%H:%M:%S"
            ), 7
        )
