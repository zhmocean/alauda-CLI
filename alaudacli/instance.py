import util
import auth
import json
import requests


class Instance(object):

    def __init__(self, service=None, uuid='', details=None):
        self.service = service
        self.uuid = uuid
        self.details = details

    @classmethod
    def fetch(cls, service, id):
        api_endpoint, token, _ = auth.load_token()
        url = api_endpoint + 'services/{0}/{1}/instances/{2}'.format(service.namespace, service.name, id)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        data = json.loads(r.text)
        instance = cls(service=service, uuid=data['uuid'], details=r.text)
        return instance

    @classmethod
    def list(cls, service):
        api_endpoint, token, _ = auth.load_token()
        url = api_endpoint + 'services/{0}/{1}/instances/'.format(service.namespace, service.name)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        data = json.loads(r.text)
        instances = []
        for instance in data:
            instance = cls(service=service, uuid=instance['uuid'])
            instances.append(instance)
        return instances

    def logs(self, start_time, end_time):
        start, end = util.parse_time(start_time, end_time)
        api_endpoint, token, _ = auth.load_token()
        url = api_endpoint + 'services/{0}/{1}/instances/{2}/logs?start_time={3}&end_time={4}'.format(self.service.namespace,
                                                                                                      self.service.name,
                                                                                                      self.uuid, start, end)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        return r.text

    def metrics(self, start_time, end_time):
        start, end = util.parse_time(start_time, end_time)
        api_endpoint, token, _ = auth.load_token()
        url = api_endpoint + 'services/{0}/{1}/instances/{2}/metrics?start_time={3}&end_time={4}'.format(self.service.namespace,
                                                                                                         self.service.name,
                                                                                                         self.uuid, start, end)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        return r.text
