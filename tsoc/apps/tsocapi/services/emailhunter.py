import requests
from django.conf import settings


class Hunter(object):
    api_key = settings.HUNTER_API_KEY #GET FROM CONFIG
    base_endpoint = "https://api.hunter.io/v2/"

    def is_email_deliverable(self, email):
        params = {'email': email, 'api_key': self.api_key}
        result = self._query_hunter(endpoint="https://api.hunter.io/v2/email-verifier", params=params)

        if result == "deliverable":
            return True
        return False

    def _query_hunter(self, endpoint, params, request_type='get',
                      payload=None, headers=None, raw=False):

        res = requests.get(url=endpoint, params=params)

        data = res.json().get("data", {}).get("result", {})
        return data


hunter_client = Hunter()
