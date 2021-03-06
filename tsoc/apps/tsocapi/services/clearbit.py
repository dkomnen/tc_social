import clearbit
from django.conf import settings


class Clearbit(object):
    api_key = settings.CLEARBIT_API_KEY  # GET FROM CONFIG
    clearbit.Person.version = '2018-11-19'
    clearbit.key = api_key

    def clearbit_data_enrichment(self, email):
        response = clearbit.Enrichment.find(email=email, stream=True)
        return response


clearbit_client = Clearbit()
