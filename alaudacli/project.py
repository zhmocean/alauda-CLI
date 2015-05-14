class Project(object):

    def __init__(self, services):
        self.services = services

    def up(self):
        for service in self.services:
            print "Creating service: {}".format(service.name)
            service.run()
