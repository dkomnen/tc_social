import requests


class Hunter(object):
    api_key = "" #GET FROM CONFIG
    base_endpoint = "https://api.hunter.io/v2/"

    def is_email_deliverable(self, email):
        params = {'email': email, 'api_key': self.api_key}
        result = self._query_hunter(endpoint="https://api.hunter.io/v2/email-verifier", params=params)
        if result == "deliverable":
            return True
        return False

    def _query_hunter(self, endpoint, params, request_type='get',
                      payload=None, headers=None, raw=False):

        # request_kwargs = dict(params=params)
        # if payload:
        #     request_kwargs.setdefault(json=payload)
        #
        # if headers:
        #     request_kwargs.setdefault(headers=headers)
        #
        # res = getattr(requests, request_type)(endpoint, **request_kwargs)
        # res.raise_for_status()
        #
        # if raw:
        #     return res
        #
        # data = res.json()['data']
        res = requests.get(url=endpoint, params=params)

        data = res.json().get("data", {}).get("result", {})
        return data


hunter_client = Hunter()
