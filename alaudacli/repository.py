import util
import auth
import json
import requests
from exceptions import AlaudaServerError


class Repository(object):

    def __init__(self, name, description='', full_description='', is_public=True, repo_clone_url='', repo_client='Simple',
                 repo_namespace='', repo_name='', tag_configs='', namespace=None, details=''):
        self.name = name
        self.description = description
        self.full_description = full_description
        self.is_public = is_public
        self.repo_client = repo_client
        self.repo_clone_url = repo_clone_url
        self.repo_namespace = repo_namespace
        self.repo_name = repo_name
        self.tag_configs = tag_configs
        self.details = details

        self.api_endpoint, self.token, self.username = auth.load_token()
        self.headers = auth.build_headers(self.token)
        self.namespace = namespace or self.username

    def create(self):
        payload = {
            'repo_name': self.name,
            'description': self.description,
            'full_description': self.full_description,
            'is_public': self.is_public,
            'build_config': {
                'code_repo_client': self.repo_client,
                'tag_configs': self.tag_configs
            }
        }
        if self.repo_client == 'Simple':
            payload['build_config']['code_repo_clone_url'] = self.repo_clone_url
        else:
            payload['build_config']['code_repo_namespace'] = self.repo_namespace
            payload['build_config']['code_repo_name'] = self.repo_name

        url = self.api_endpoint + 'repositories/{}/'.format(self.namespace)
        r = requests.post(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)
        return r.text

    @classmethod
    def fetch(cls, name, namespace=None):
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'repositories/{}/{}/'.format(namespace or username, name)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        data = json.loads(r.text)
        repo = cls(name=data['repo_name'], is_public=data['is_public'], repo_client=data['build_config']['code_repo_client'],
                   repo_namespace=data['build_config']['created_by'],
                   repo_name=str(data['build_config']['docker_repo_path'])[len(data['build_config']['created_by']) + 1:],
                   namespace=data['namespace'], details=r.text)
        return repo

    @classmethod
    def list(cls, namespace=None):
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'repositories/{}/'.format(namespace or username)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        repos_list = []
        repos = json.loads(r.text)
        repos = repos.get('results', [])
        for data in repos:
            try:
                repo = Repository.fetch(data['repo_name'], namespace)
                repos_list.append(repo)
            except AlaudaServerError:
                continue
        return repos_list

    @classmethod
    def remove(cls, name, namespace=None):
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'repositories/{}/{}/'.format(namespace or username, name)
        headers = auth.build_headers(token)
        try:
            r = requests.delete(url, headers=headers)
            util.check_response(r)
        except AlaudaServerError as ex:
            if ex.status_code == 404:
                print '[alauda] Repository "{}" does not exist'.format(name)
            else:
                raise ex

    def inspect(self):
        return self.details

    def update(self, description, full_description):
        payload = {}
        if description is not None:
            payload['description'] = description
        if full_description is not None:
            payload['full_description'] = full_description
        url = self.api_endpoint + 'repositories/{}/{}'.format(self.namespace, self.name)
        r = requests.put(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)

    def public(self):
        payload = {'is_public': True}
        url = self.api_endpoint + 'repositories/{}/{}'.format(self.namespace, self.name)
        r = requests.put(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)

    def private(self):
        payload = {'is_public': False}
        url = self.api_endpoint + 'repositories/{}/{}'.format(self.namespace, self.name)
        r = requests.put(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)

    def merge_tags(self, tag_config=None):
        url = self.api_endpoint + 'repositories/{0}/{1}/tag-configs-merge'.format(self.namespace, self.name)
        r = requests.post(url, headers=self.headers, data=json.dumps(tag_config))
        util.check_response(r)

    def list_tags(self):
        url = self.api_endpoint + 'repositories/{0}/{1}/tags'.format(self.namespace, self.name)
        r = requests.get(url, headers=self.headers)
        util.check_response(r)
        return r.text

    def inspect_tag(self, tag):
        url = self.api_endpoint + 'repositories/{0}/{1}/tags/{2}'.format(self.namespace, self.name, tag)
        r = requests.get(url, headers=self.headers)
        util.check_response(r)
        return r.text
