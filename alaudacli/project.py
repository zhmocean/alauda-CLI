from service import Service


class Project(object):

    def __init__(self, services, sorted_name):
        self.services = services
        self.sorted_name = sorted_name

    def up(self):
        for service in self.services:
            print "Creating service: {}".format(service.name)
            service.run()

    def _format_ps_output(self, service_list):
        max_name_len = len('Name')
        max_command_len = len('Command')
        max_state_len = len('State')
        max_ports_len = len('Ports')

        for service in service_list:
            if max_name_len < len(service.name):
                max_name_len = len(service.name)
            run_command = service.get_run_command()
            if max_command_len < len(run_command):
                max_command_len = len(run_command)
            state = service.get_state()
            if max_state_len < len(state):
                max_state_len = len(state)
            ports = service.get_ports()
            if max_ports_len < len(ports):
                max_ports_len = len(ports)
        return max_name_len, max_command_len, max_state_len, max_ports_len

    def ps(self):
        service_list = Service.get_service_list(self.sorted_name)
        name_len, command_len, state_len, ports_len = self._format_ps_output(service_list)
        print '{0}    {1}    {2}    {3}'.format('Name'.center(name_len), 'Command'.center(command_len), 'State'.center(state_len), 'Ports'.center(ports_len))
        print '{0}'.format('-' * (name_len + command_len + state_len + ports_len + 3 * 4))
        for service in service_list:
            print '{0}    {1}    {2}    {3}'.format(service.name.ljust(name_len), service.get_run_command().ljust(command_len),
                                                    service.get_state().ljust(state_len), service.get_ports().ljust(ports_len))

    def start(self):
        for service in self.services:
            service.start()

    def stop(self):
        for service in self.services:
            service.stop()

    def rm(self):
        for name in self.sorted_name:
            Service.remove(name)

    def scale(self, scale_dict):
        for name, number in scale_dict.items():
            service = Service.fetch(name)
            service.update(number)
