import util
import auth
import json
import requests


class Build(object):

    def __init__(self, build_id, details):
        self.build_id = build_id
        self.details = details

        self.api_endpoint, self.token, self.username = auth.load_token()
        self.headers = auth.build_headers(self.token)

    @classmethod
    def trigger(cls, name, namespace, tag):
        api_endpoint, token, username = auth.load_token()
        headers = auth.build_headers(token)
        payload = {
            'namespace': namespace or username,
            'repo_name': name,
            'tag': tag
        }
        print 'payloads:{}'.format(payload)
        url = api_endpoint + 'builds/'
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        util.check_response(r)
        print r.text

    @classmethod
    def fetch(cls, build_id):
        api_endpoint, token, _ = auth.load_token()
        headers = auth.build_headers(token)
        url = api_endpoint + 'builds/{}'.format(build_id)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        data = json.loads(r.text)
        build = cls(build_id=data['build_id'], details=r.text)
        return build

    def logs(self, start_time, end_time):
        start, end = util.parse_time(start_time, end_time)
        url = self.api_endpoint + 'builds/{0}/logs?start_time={1}&end_time={2}'.format(self.build_id, start, end)
        r = requests.get(url, headers=self.headers)
        util.check_response(r)
        return r.text

    @classmethod
    def remove(cls, build_id):
        api_endpoint, token, _ = auth.load_token()
        headers = auth.build_headers(token)
        url = api_endpoint + 'builds/{}'.format(build_id)
        r = requests.delete(url, headers=headers)
        util.check_response(r)
        return r.text

    @classmethod
    def list(cls, page):
        api_endpoint, token, _ = auth.load_token()
        headers = auth.build_headers(token)
        url = api_endpoint + 'builds/?page={}'.format(page)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        builds = json.loads(r.text)
        builds = builds.get('results', [])
        build_list = []
        for data in builds:
            build = Build.fetch(data['build_id'])
            build_list.append(build)
        return build_list

    def inspect(self):
        return self.details
