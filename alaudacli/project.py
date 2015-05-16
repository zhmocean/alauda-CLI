from service import Service
import util
import time


class Project(object):

    def __init__(self, services):
        self.services = services

    def up(self):
        for service in self.services:
            print "Creating and starting service: {}".format(service.name)
            service.run()
            time.sleep(1)

    def ps(self):
        service_list = self._get_service_list()
        util.print_ps_output(service_list)

    def start(self):
        for service in self.services:
            print "Starting service: {}".format(service.name)
            service.start()

    def stop(self):
        for service in self.services:
            print "Stoping service: {}".format(service.name)
            service.stop()

    def restart(self):
        for service in self.services:
            print "Stoping service: {}".format(service.name)
            service.stop()
        for service in self.services:
            print "Starting service: {}".format(service.name)
            service.start()

    def rm(self):
        for service in self.services:
            print "Removing service: {}".format(service.name)
            Service.remove(service.name)

    def scale(self, scale_dict):
        for name, number in scale_dict.items():
            print "Scaling service: {0} -> {1}".format(name, number)
            service = Service.fetch(name)
            service.update(number)

    def _get_service_list(self):
        service_list = []
        for service in self.services:
            try:
                service_list.append(service.fetch(service.name))
            except ValueError:
                continue
        return service_list
