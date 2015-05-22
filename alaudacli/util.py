from exceptions import AlaudaInputError, AlaudaServerError
import json


def parse_image_name_tag(image):
    result = image.split(':')
    if len(result) == 1:
        return image, 'latest'
    elif len(result) == 2:
        return result[0], result[1]
    else:
        raise AlaudaInputError('Invalid image name')


def parse_target_state(start):
    if start:
        return 'STARTED'
    else:
        return 'STOPPED'


def parse_instance_ports(port_list):
    def _parse_instance_port(_port):
        result = _port.split('/')
        if len(result) > 2:
            raise AlaudaInputError('Invalid port description. (Example of valid description: 80/tcp)')

        try:
            port = int(result[0])
        except:
            raise AlaudaInputError('Invalid port description. (Example of valid description: 80/tcp)')

        if len(result) == 2:
            protocol = result[1]
        else:
            protocol = 'tcp'

        if protocol not in ['tcp']:
            raise AlaudaInputError('Invalid port protocal. Supported protocols: {tcp}')
        if port < 0 or port > 65535:
            raise AlaudaInputError('Invalid port number')

        return port, protocol

    parsed_ports = []
    if port_list is not None:
        for port_desc in port_list:
            port, protocol = _parse_instance_port(port_desc)
            parsed_ports.append({"container_port": port, "protocol": protocol})
    return parsed_ports


def parse_envvar(_envvar):
    def _parse_envvar_dict(_envvar):
        if len(_envvar) != 1:
            raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')
        key = _envvar.keys()[0]
        value = _envvar[key]
        if value is None:
            value = ''
        return key, str(value)

    def _parse_envvar_str(_envvar):
        pos = _envvar.find('=')
        if pos != -1:
            key = _envvar[:pos]
            value = _envvar[pos + 1:]
            return key, value
        else:
            pos = _envvar.find(':')
            if pos == -1:
                raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')
            key = _envvar[:pos]
            value = _envvar[pos + 1:]
            return key, value

    if isinstance(_envvar, dict):
        return _parse_envvar_dict(_envvar)
    elif isinstance(_envvar, str):
        return _parse_envvar_str(_envvar)
    else:
        raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')


def parse_envvars(envvar_list):
    #     def _parse_envvar_dict(_envvar):
    #         if len(_envvar) != 1:
    #             raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')
    #         key = _envvar.keys()[0]
    #         value = _envvar[key]
    #         if value is None:
    #             value = ''
    #         return key, str(value)
    #
    #     def _parse_envvar_str(_envvar):
    #         pos = _envvar.find('=')
    #         if pos != -1:
    #             key = _envvar[:pos]
    #             value = _envvar[pos + 1:]
    #             return key, value
    #         else:
    #             pos = _envvar.find(':')
    #             if pos == -1:
    #                 raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')
    #             key = _envvar[:pos]
    #             value = _envvar[pos + 1:]
    #             return key, value
    #
    #     def _parse_envvar(_envvar):
    #         if isinstance(_envvar, dict):
    #             return _parse_envvar_dict(_envvar)
    #         elif isinstance(_envvar, str):
    #             return _parse_envvar_str(_envvar)
    #         else:
    #             raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')

    parsed_envvars = {}
    if envvar_list is not None:
        for envvar in envvar_list:
            key, value = parse_envvar(envvar)
            parsed_envvars[key] = value
    return parsed_envvars


def parse_volume(_volume):
    if not isinstance(_volume, str):
        raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')
    result = _volume.split(':')
    if len(result) != 2 and len(result) != 3:
        raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')

    path = result[0]
    try:
        size = int(result[1])
        backup_id = None
        if len(result) == 3:
            backup_id = result[2]
    except:
        print "except"
        raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')
    return path, size, backup_id


def parse_volumes(volume_list):
    #     def _parse_volume(_volume):
    #         if not isinstance(_volume, str):
    #             raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')
    #         result = _volume.split(':')
    #         if len(result) != 2 and len(result) != 3:
    #             raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')
    #
    #         path = result[0]
    #         try:
    #             size = int(result[1])
    #             backup_id = None
    #             if len(result) == 3:
    #                 backup_id = result[2]
    #         except:
    #             print "except"
    #             raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')
    #         return path, size, backup_id

    parsed_volumes = []
    if volume_list is not None:
        for volume_desc in volume_list:
            path, size, backup_id = parse_volume(volume_desc)
            volume = {"app_volume_dir": path, "size_gb": size, "volume_type": "EBS"}
            if backup_id is not None:
                volume['backup_id'] = backup_id
            parsed_volumes.append(volume)
    return parsed_volumes


def parse_links(link_list):
    def _parse_link(_link):
        if not isinstance(_link, str):
            raise AlaudaInputError('Invalid link description. (Example of valid description: mysql:db)')
        result = _link.split(':')
        if len(result) > 2:
            raise AlaudaInputError('Invalid link description. (Example of valid description: mysql:db)')
        if len(result) == 1 or len(result[1]) == 0:
            return result[0], result[0]
        return result[0], result[1]

    parsed_links = []
    if link_list is not None:
        for link in link_list:
            service_name, alias = _parse_link(link)
            parsed_links.append((service_name, alias))
    return parsed_links


def parse_scale(name_number_list):
    def _parse_scale(_name_number):
        result = _name_number.split('=')
        if len(result) != 2:
            raise AlaudaInputError('Invalid scale description. (Example of valid description: mysql=3)')

        name = result[0]
        try:
            number = int(result[1])
        except:
            raise AlaudaInputError('Invalid scale description. (Example of valid description: mysql=3)')
        return name, number

    scale_dict = {}
    for name_number in name_number_list:
        name, number = _parse_scale(name_number)
        scale_dict[name] = number
    return scale_dict


def parse_autoscale_info(info):
    if info is None:
        return 'MANUAL', {}
    mode = info[0]
    cfg_file = info[1]
    if mode:
        try:
            fp = file(cfg_file)
        except:
            raise AlaudaInputError('can not open auto-scaling config file-> {}.'.format(cfg_file))
        try:
            cfg_json = json.load(fp)
            fp.close()
        except:
            fp.close()
            raise AlaudaInputError('Parse {} fail! The format refer to ./auto-scaling.example'.format(cfg_file))
        return 'AUTO', json.dumps(cfg_json)
    else:
        return 'MANUAL', {}


def failed(status_code):
    return status_code < 200 or status_code >= 300


def check_response(response):
    if failed(response.status_code):
        raise AlaudaServerError(response.status_code, response.text)


def print_ps_output(service_list):
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


def print_backup_ps_output(backup_list):
    max_name_len = len('Name')
    max_id_len = len('Id')
    max_state_len = len('State')
    max_time_len = len('Created time')
    max_size_len = len('Size')

    for data in backup_list:
        backup = json.loads(data.details)
        if max_name_len < len(backup['name']):
            max_name_len = len(backup['name'])
        if max_id_len < len(backup['backup_id']):
            max_id_len = len(backup['backup_id'])
        if max_state_len < len(backup['status']):
            max_state_len = len(backup['status'])
        if max_time_len < len(backup['created_datetime']):
            max_time_len = len(backup['created_datetime'])
        size_byte = backup.get('size_byte', ' ')
        if max_size_len < len(str(size_byte)):
            max_size_len = len(str(size_byte))

    print '{0}    {1}    {2}    {3}    {4}'.format('Id'.center(max_id_len), 'Name'.center(max_name_len), 'State'.center(max_state_len),
                                                   'Size'.center(max_size_len), 'Created time'.center(max_time_len))
    print '{0}'.format('-' * (max_id_len + max_name_len + max_state_len + max_time_len + max_size_len + 4 * 4))

    for data in backup_list:
        backup = json.loads(data.details)
        print '{0}    {1}    {2}    {3}    {4}'.format(str(backup['backup_id']).ljust(max_id_len), str(backup['name']).ljust(max_name_len),
                                                       str(backup['status']).ljust(max_state_len), str(backup.get('size_byte', ' ')).ljust(max_size_len),
                                                       str(backup['created_datetime']).ljust(max_time_len))


def indegree0(v, e):
    if v == []:
        return None
    tmp = v[:]
    for i in e:
        if i[1] in tmp:
            tmp.remove(i[1])
    if tmp == []:
        return -1

    for t in tmp:
        for i in range(len(e)):
            if t in e[i]:
                e[i] = 'toDel'
    if e:
        eset = set(e)
        eset.remove('toDel')
        e[:] = list(eset)
    if v:
        for t in tmp:
            v.remove(t)
    return tmp


def topoSort(v, e):
    result = []
    while True:
        nodes = indegree0(v, e)
        if nodes is None:
            break
        if nodes == -1:
            print('there\'s a circle.')
            return None
        result.extend(nodes)
    return result
