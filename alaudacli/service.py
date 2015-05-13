import json
import requests

import auth


class Service(object):
    def __init__(self, name, image_name, image_tag, target_num_instances, instance_size, run_command='',
                 instance_ports=None, instance_envvars=None, allocation_group='', details=''):
        self.name = name
        self.image_name = image_name
        self.image_tag = image_tag
        self.target_num_instances = target_num_instances
        self.instance_size = instance_size
        self.run_command = run_command
        self.instance_envvars = instance_envvars
        self.instance_ports = instance_ports
        self.allocation_group = allocation_group
        self.details = details

        self.api_endpoint, self.token = auth.load_token()
        self.headers = auth.build_headers(self.token)

    def _create_remote(self, target_state):
        url = self.api_endpoint + 'apps/'
        payload = {
            "app_name": self.name,
            "target_num_instances": self.target_num_instances,
            "image_name": self.image_name,
            "image_tag": self.image_tag,
            "instance_size": self.instance_size,
            "scaling_mode": "MANUAL",
            "target_state": target_state,
            "run_command": self.run_command,
            "instance_envvars": self.instance_envvars,
            "instance_ports": self.instance_ports,
            "allocation_group": self.allocation_group,
        }
        r = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return r

    @classmethod
    def fetch(cls, name):
        api_endpoint, token = auth.load_token()
        url = api_endpoint + 'apps/' + name
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
        service = cls(name=data['service_name'],
                      image_name=data['image_name'],
                      image_tag=data['image_tag'],
                      target_num_instances=data['target_num_instances'],
                      instance_size=data['instance_size'],
                      details=r.text)
        return service

    @classmethod
    def list(cls):
        api_endpoint, token = auth.load_token()
        url = api_endpoint + 'apps/'
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        return r

    @classmethod
    def remove(cls, name):
        api_endpoint, token = auth.load_token()
        url = api_endpoint + 'apps/' + name
        headers = auth.build_headers(token)
        r = requests.delete(url, headers=headers)
        return r

    def create(self):
        return self._create_remote('STOPPED')

    def run(self):
        return self._create_remote('STARTED')

    def inspect(self):
        return self.details

    def start(self):
        self.target_state = 'STARTED'
        url = self.api_endpoint + 'apps/' + self.name + '/start/'
        r = requests.put(url, headers=self.headers)
        return r

    def stop(self):
        self.target_state = 'STOPPED'
        url = self.api_endpoint + 'apps/' + self.name + '/stop/'
        r = requests.put(url, headers=self.headers)
        return r

    def update(self, target_num_instances):
        self.target_num_instances = target_num_instances
        url = self.api_endpoint + 'apps/' + self.name
        payload = {
            "app_name": self.name,
            "target_num_instances": self.target_num_instances
        }
        r = requests.put(url, headers=self.headers, data=json.dumps(payload))
        return r
