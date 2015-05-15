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


def parse_envvars(envvar_list, split_flag):
    def _parse_envvar(_envvar):
        if isinstance(_envvar, dict):
            if len(_envvar) != 1:
                print 'Invalid environment variable'
                sys.exit(1)
            key = _envvar.keys()[0]
            value = _envvar[key]
            if value is None:
                value = ''
            return key, str(value)
        result = _envvar.split(split_flag)
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
        if isinstance(_volume, dict):
            if len(_volume) != 1:
                print 'Invalid environment variable'
                sys.exit(1)
            path = _volume.keys()[0]
            try:
                size = int(_volume[path])
            except:
                print 'Invalid volume description. (Example of valid description: /var/lib/data1:10)'
                sys.exit(1)
            return path, size
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


def parse_scale(name_number_list):
    def _parse_scale(_name_number):
        result = _name_number.split('=')
        if len(result) != 2:
            print 'Invalid scale description. (Example of valid description: mysql=3)'
            sys.exit(1)

        name = result[0]
        try:
            number = int(result[1])
        except:
            print 'Invalid scale description. (Example of valid description: mysql=3)'
            sys.exit(1)
        return name, number

    scale_dict = {}
    for name_number in name_number_list:
        name, number = _parse_scale(name_number)
        scale_dict[name] = number
    return scale_dict


def failed(status_code):
    return status_code < 200 or status_code >= 300


def check_response(response):
    if failed(response.status_code):
        print '[error]: {0} {1}'.format(response.status_code, response.text)
        sys.exit(1)


def format_ps_output(service_list):
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

    print '{0}    {1}    {2}    {3}    {4}'.format('Name'.center(max_name_len), 'Command'.center(max_command_len), 'State'.center(max_state_len),
                                                   'Ports'.center(max_ports_len), 'Instance Count'.center(max_instance_count_len))
    print '{0}'.format('-' * (max_name_len + max_command_len + max_state_len + max_ports_len + max_instance_count_len + 4 * 4))
    for service in service_list:
        print '{0}    {1}    {2}    {3}    {4}'.format(service.name.ljust(max_name_len), service.get_run_command().ljust(max_command_len),
                                                       service.get_state().ljust(max_state_len), service.get_ports().ljust(max_ports_len),
                                                       str(service.target_num_instances).ljust(max_instance_count_len))
