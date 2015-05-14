import json
import requests

import auth
import util


class Service(object):

    def __init__(self, name, image_name, image_tag, target_num_instances=1, instance_size='XS', run_command='',
                 instance_ports=None, instance_envvars=None, allocation_group='', volumes=None, links=None, details=''):
        self.name = name
        self.image_name = image_name
        self.image_tag = image_tag
        self.target_num_instances = target_num_instances
        self.instance_size = instance_size
        self.run_command = run_command
        self.instance_envvars = util.parse_envvars(instance_envvars)
        self.instance_ports = instance_ports
        self.allocation_group = allocation_group
        self.volumes = volumes
        self.links = links
        self.details = details

        self.api_endpoint, self.token = auth.load_token()
        self.headers = auth.build_headers(self.token)

    def _update_envvars_with_links(self, instance_envvars, links):
        link_to = {}
        if links is not None:
            for link in links:
                service_name = link[0]
                alias = link[1]
                link_to[service_name] = alias
                linked_service = Service.fetch(service_name)
                linked_service_data = json.loads(linked_service.details)
                linked_service_ports = linked_service_data['instance_ports']
                linked_service_envvars = json.loads(linked_service_data['instance_envvars'])
                linked_service_addr = linked_service_envvars['__DEFAULT_DOMAIN_NAME__']
                key = '{0}_PORT'.format(alias).upper()
                for port in linked_service_ports:
                    url = '{0}://{1}:{2}'.format(port['protocol'], linked_service_addr, port['service_port'])
                    if key not in instance_envvars.keys():
                        instance_envvars[key] = url
                    pattern = '{0}_PORT_{1}_{2}'.format(alias, port['container_port'], port['protocol']).upper()
                    instance_envvars[pattern] = url
                    instance_envvars[pattern + '_ADDR'] = linked_service_addr
                    instance_envvars[pattern + '_PORT'] = str(port['service_port'])
                    instance_envvars[pattern + '_PROTO'] = port['protocol']
        return link_to

    def _create_remote(self, target_state):
        link_to = self._update_envvars_with_links(self.instance_envvars, self.links)
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
            'linked_to': link_to
            #             "volumes": self.volumes
        }
        if self.volumes is not None:
            payload['volumes'] = self.volumes
        r = requests.post(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)

    @classmethod
    def fetch(cls, name):
        api_endpoint, token = auth.load_token()
        url = api_endpoint + 'apps/' + name
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
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
        util.check_response(r)
        return r.text

    @classmethod
    def remove(cls, name):
        api_endpoint, token = auth.load_token()
        url = api_endpoint + 'apps/' + name
        headers = auth.build_headers(token)
        r = requests.delete(url, headers=headers)
        util.check_response(r)

    def create(self):
        self._create_remote('STOPPED')

    def run(self):
        self._create_remote('STARTED')

    def inspect(self):
        if not self.details:
            url = self.api_endpoint + 'apps/' + self.name
            r = requests.get(url, headers=self.headers)
            util.check_response(r)
            self.details = r.text
        return self.details

    def start(self):
        self.target_state = 'STARTED'
        url = self.api_endpoint + 'apps/' + self.name + '/start/'
        r = requests.put(url, headers=self.headers)
        util.check_response(r)

    def stop(self):
        self.target_state = 'STOPPED'
        url = self.api_endpoint + 'apps/' + self.name + '/stop/'
        r = requests.put(url, headers=self.headers)
        util.check_response(r)

    def update(self, target_num_instances):
        self.target_num_instances = target_num_instances
        url = self.api_endpoint + 'apps/' + self.name
        payload = {
            "app_name": self.name,
            "target_num_instances": self.target_num_instances
        }
        r = requests.put(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)
