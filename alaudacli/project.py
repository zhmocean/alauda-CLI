import json


class Project(object):

    def __init__(self, services):
        self.services = services

    def up(self):
        for service in self.services:
            print "Creating service: {}".format(service.name)
            service.run()

    def _get_service_state(self, service):
        data = json.loads(service.details)
        if data['is_deploying']:
            return 'Deploying'
        if data['current_num_instances'] == data['target_num_instances']:
            return 'Running'
        elif data['target_state'] == 'STOPPED':
            return 'Stopped'
        else:
            return 'Error'

    def _get_service_ports(self, service):
        ports = ''
        data = json.loads(service.details)
        if len(data['instance_ports']) == 0:
            return ' '
        for port in data['instance_ports']:
            instance_envvars = json.loads(data['instance_envvars'])
            ports = ports + '{0}:{1}->{2}/{3}, '.format(instance_envvars['__DEFAULT_DOMAIN_NAME__'],
                                                        port['service_port'],
                                                        port['container_port'],
                                                        port['protocol'])
        return ports[:len(ports) - 2]

    def _get_service_run_command(self, service):
        data = json.loads(service.details)
        run_command = str(data['run_command'])
        if len(run_command) == 0:
            run_command = ' '
        return run_command

    def _get_service_list(self):
        service_list = []
        for service in self.services:
            service_list.append(service.fetch(service.name))
        return service_list

    def _format_ps_output(self, service_list):
        max_name_len = len('Name')
        max_command_len = len('Command')
        max_state_len = len('State')
        max_ports_len = len('Ports')

        for service in service_list:
            if max_name_len < len(service.name):
                max_name_len = len(service.name)
            run_command = self._get_service_run_command(service)
            if max_command_len < len(run_command):
                max_command_len = len(run_command)
            state = self._get_service_state(service)
            if max_state_len < len(state):
                max_state_len = len(state)
            ports = self._get_service_ports(service)
            if max_ports_len < len(ports):
                max_ports_len = len(ports)
        return max_name_len, max_command_len, max_state_len, max_ports_len

    def ps(self):
        service_list = self._get_service_list()
        name_len, command_len, state_len, ports_len = self._format_ps_output(service_list)
        print '{0}    {1}    {2}    {3}'.format('Name'.center(name_len), 'Command'.center(command_len), 'State'.center(state_len), 'Ports'.center(ports_len))
        print '{0}'.format('-' * (name_len + command_len + state_len + ports_len + 3 * 4))
        for service in service_list:
            print '{0}    {1}    {2}    {3}'.format(service.name.ljust(name_len), self._get_service_run_command(service).ljust(command_len),
                                                    self._get_service_state(service).ljust(state_len), self._get_service_ports(service).ljust(ports_len))
