import getpass
import sys
import traceback

import paramiko
import interactive
import auth
import util
import json
import requests


class Executer(object):

    def __init__(self, name, namespace, exec_endpoint='exec.alauda.cn', port=4022, verbose=False):
        self.name = name
        self.namespace = namespace
        self.exec_endpoint = exec_endpoint
        self.port = port
        self.client = None
        self.chan = None
        self.verbose = verbose

    def connect(self):
        if self.verbose:
            print('*** Connecting...')

        # connect to the exec_endpoint
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        password = getpass.getpass('Password for %s@%s: ' % (self.namespace, self.exec_endpoint))
        self.client.connect(self.exec_endpoint,
                            self.port,
                            username=self.namespace,
                            password=password,
                            allow_agent=False,
                            look_for_keys=False)

        if self.verbose:
            print(repr(self.client.get_transport()))

    def execute(self, command, *args):
        try:
            self.connect()
            transport = self.client.get_transport()
            self.chan = transport.open_session()
            self.chan.get_pty()
            self.chan.exec_command('{} {} {}'.format(self.name, command, ' '.join(args)))
            interactive.interactive_shell(self.chan)
            self.close()
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.close()
            except:
                pass
            sys.exit(1)

    def close(self):
        if self.chan:
            self.chan.close()
        self.client.close()

    @classmethod
    def fetch(cls, name, namespace=None):
        service_name = name.split(".")[0]

        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'services/{}/'.format(namespace or username) + service_name
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        data = json.loads(r.text)
        # print r.text
        executer = cls(name=name,
                       exec_endpoint=data['exec_endpoint'],
                       namespace=data['namespace'])
        return executer
