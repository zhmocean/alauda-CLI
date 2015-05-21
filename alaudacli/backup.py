import util
import auth
import json
import requests
from exceptions import AlaudaServerError


class Backup(object):

    def __init__(self, service):
        self.service = service

    def create(self, name, mounted_dir):
        print '[alauda] Creating backup "{}"'.format(name)
        data = json.loads(self.service.details)
        uuid = data['unique_name']
        url = self.service.api_endpoint + 'backups/{}/'.format(self.service.namespace)
        payload = {
            'app_id': uuid,
            'name': name,
            'app_volume_dir': mounted_dir
        }
        r = requests.post(url, headers=self.service.headers, data=json.dumps(payload))
        util.check_response(r)

    @classmethod
    def list(cls, namespace=None):
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'backups/{}/'.format(namespace or username)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        backup_list = json.loads(r.text)
        return backup_list

    @classmethod
    def inspect(cls, id, namespace=None):
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'backups/{0}/{1}/'.format(namespace or username, id)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        try:
            util.check_response(r)
            return r.text
        except AlaudaServerError as ex:
            if ex.status_code == 400:
                print '[alauda] backup "{}" does not exist'.format(id)
            else:
                raise ex

    @classmethod
    def remove(cls, id, namespace=None):
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'backups/{0}/{1}/'.format(namespace or username, id)
        headers = auth.build_headers(token)
        r = requests.delete(url, headers=headers)
        try:
            util.check_response(r)
        except AlaudaServerError as ex:
            if ex.status_code == 400:
                print '[alauda] backup "{}" does not exist'.format(id)
            else:
                raise ex
