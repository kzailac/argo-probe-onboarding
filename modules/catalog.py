import datetime

import requests


class CriticalException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


def get_today():
    return datetime.datetime.now()


class CatalogAPI:
    def __init__(self, url, catalog_id):
        self.url = url
        self.catalog_id = catalog_id
        self.data = self._get_data()

    def _get_data(self):
        if self.url.endswith("/"):
            url = f"{self.url}{self.catalog_id}"

        else:
            url = f"{self.url}/{self.catalog_id}"

        try:
            response = requests.get(url)

            response.raise_for_status()

            if response.ok:
                return response.json()

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects
        ) as e:
            raise CriticalException(e)

    def check_key_exists(self, key):
        return key in self.data

    def check_url_valid(self, key):
        response = requests.get(self.data[key])
        if response.ok:
            return True

        else:
            return False

    def check_date_age(self, key, date_format):
        def age_month(d):
            today = get_today()
            return (today.year - d.year) * 12 + today.month - d.month

        datetime_object = datetime.datetime.strptime(
            self.data[key], date_format
        )

        return age_month(datetime_object)
