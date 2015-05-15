from service import Service
import util


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
        max_instance_count_len = len('Instance Count')

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
            if max_instance_count_len < len(str(service.target_num_instances)):
                max_instance_count_len = len(str(service.target_num_instances))
        return max_name_len, max_command_len, max_state_len, max_ports_len, max_instance_count_len

    def ps(self):
        service_list = Service.get_service_list(self.sorted_name)
        util.format_ps_output(service_list)

    def start(self):
        for service in self.services:
            print "Starting services: {}".format(service.name)
            service.start()

    def stop(self):
        for service in self.services:
            print "Stoping services: {}".format(service.name)
            service.stop()

    def restart(self):
        for service in self.services:
            print "Stoping services: {}".format(service.name)
            service.stop()
        for service in self.services:
            print "Starting services: {}".format(service.name)
            service.start()

    def rm(self):
        for name in self.sorted_name:
            Service.remove(name)

    def scale(self, scale_dict):
        for name, number in scale_dict.items():
            service = Service.fetch(name)
            service.update(number)
