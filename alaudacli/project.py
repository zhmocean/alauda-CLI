from service import Service
import util
from exceptions import AlaudaServerError


class Project(object):

    def __init__(self, services):
        self.services = services

    def up(self):
        for service in self.services:
            service.run()

    def ps(self):
        service_list = self._get_service_list()
        util.print_ps_output(service_list)

    def start(self):
        for service in self.services:
            service.start()

    def stop(self):
        for service in self.services:
            service.stop()

    def restart(self):
        for service in self.services:
            service.stop()
        for service in self.services:
            service.start()

    def rm(self):
        for service in self.services:
            Service.remove(service.name)

    def scale(self, scale_dict):
        for name, number in scale_dict.items():
            service = Service.fetch(name)
            service.update(number)

    def _get_service_list(self):
        service_list = []
        for service in self.services:
            try:
                service_list.append(service.fetch(service.name))
            except AlaudaServerError:
                continue
        return service_list
