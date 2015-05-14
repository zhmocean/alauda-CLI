import sys


def parse_image_name_tag(image):
    result = image.split(':')
    if len(result) == 1:
        return image, 'latest'
    elif len(result) == 2:
        return result[0], result[1]
    else:
        print 'Invalid image name'
        sys.exit(1)


def parse_target_state(start):
    if start:
        return 'STARTED'
    else:
        return 'STOPPED'


def parse_instance_ports(port_list):
    def _parse_instance_port(_port):
        result = _port.split('/')
        if len(result) > 2:
            print 'Invalid port description. (Example of valid description: 80/tcp)'
            sys.exit(1)

        try:
            port = int(result[0])
        except:
            print 'Invalid port description. (Example of valid description: 80/tcp)'
            sys.exit(1)

        if len(result) == 2:
            protocol = result[1]
        else:
            protocol = 'tcp'

        if protocol not in ['tcp']:
            print 'Invalid port protocal. Supported protocols: {tcp}'
            sys.exit(1)
        if port < 0 or port > 65535:
            print 'Invalid port number'
            sys.exit(1)

        return port, protocol

    parsed_ports = []
    if port_list is not None:
        for port_desc in port_list:
            port, protocol = _parse_instance_port(port_desc)
            parsed_ports.append({"container_port": port, "protocol": protocol})
    return parsed_ports


def parse_envvars(envvar_list):
    def _parse_envvar(_envvar):
        result = _envvar.split('=')
        if len(result) != 2:
            print 'Invalid environment variable'
            sys.exit(1)
        return result[0], result[1]

    parsed_envvars = {}
    if envvar_list is not None:
        for envvar in envvar_list:
            key, value = _parse_envvar(envvar)
            parsed_envvars[key] = value
    return parsed_envvars


def parse_volumes(volume_list):
    def _parse_volume(_volume):
        result = _volume.split(':')
        if len(result) != 2:
            print 'Invalid volume description. (Example of valid description: /var/lib/data1:10)'
            sys.exit(1)

        path = result[0]
        try:
            size = int(result[1])
        except:
            print 'Invalid volume description. (Example of valid description: /var/lib/data1:10)'
            sys.exit(1)
        return path, size

    parsed_volumes = []
    if volume_list is not None:
        for volume_desc in volume_list:
            path, size = _parse_volume(volume_desc)
            parsed_volumes.append({"app_volume_dir": path, "size_gb": size, "volume_type": "EBS"})
    return parsed_volumes


def parse_links(link_list):
    def _parse_link(_link):
        result = _link.split(':')
        if len(result) > 2:
            print 'Invalid link description. (Example of valid description: mysql:db)'
            sys.exit(1)
        if len(result) == 1 or len(result[1]) == 0:
            return result[0], result[0]
        return result[0], result[1]

    parsed_links = []
    if link_list is not None:
        for link in link_list:
            service_name, alias = _parse_link(link)
            parsed_links.append((service_name, alias))
    else:
        return None
    return parsed_links


def failed(status_code):
    return status_code < 200 or status_code >= 300


def check_response(response):
    if failed(response.status_code):
        print '[error]: {0} {1}'.format(response.status_code, response.text)
        sys.exit(1)
