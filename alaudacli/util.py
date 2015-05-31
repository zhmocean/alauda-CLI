# -*- coding: utf-8 -*-
from exceptions import AlaudaInputError, AlaudaServerError
import json
import time
from string import Template
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

VOLUME_MIN_SIZE = 10
VOLUME_MAX_SIZE = 100


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
        if size < VOLUME_MIN_SIZE or size > VOLUME_MAX_SIZE:
            raise AlaudaInputError(
                'Invalid volume size {0}. Volume size must be between {1} and {2}'.format(
                    size,
                    VOLUME_MIN_SIZE,
                    VOLUME_MAX_SIZE))
        backup_id = None
        if len(result) == 3:
            backup_id = result[2]
    except AlaudaInputError as ex:
        raise ex
    except:
        print "except"
        raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')
    return path, size, backup_id


def parse_volumes(volume_list):
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


def load_tag_config_file(tag_config_file):
    try:
        fp = file(tag_config_file)
    except:
        raise AlaudaInputError('can not open create repo config file-> {}.'.format(tag_config_file))
    try:
        cfg_json = json.load(fp)
        fp.close()
        return cfg_json
    except:
        fp.close()
        raise AlaudaInputError('Parse {} fail! The format refer to ./create_repo_config.example or ./update_repo_config.example'.format(tag_config_file))


def parse_time(start_time, end_time):
    if start_time is not None and end_time is not None:
        try:
            start = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            start = int(time.mktime(start))
            end = int(time.mktime(end))
            return start, end
        except:
            raise AlaudaInputError('Please make sure time format like 2015-05-01 12:00:00')
    elif start_time is None and end_time is None:
        end = int(time.time())
        start = end - 900
    elif start_time is not None:
        start = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        start = int(time.mktime(start))
        end = int(time.time())
    else:
        end = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        end = int(time.mktime(end))
        start = end - 900
    return start, end


def failed(status_code):
    return status_code < 200 or status_code >= 300


def check_response(response):
    if failed(response.status_code):
        raise AlaudaServerError(response.status_code, response.text)


def expand_environment(envvars):
    for key, value in envvars.items():
        expanded = Template(value).safe_substitute(envvars)
        envvars[key] = expanded


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


def print_instance_ps_output(instance_list):
    max_name_len = len('Name')
    max_id_len = len('ID')
    max_time_len = len('Created time')

    for data in instance_list:
        instance = json.loads(data.details)
        if max_name_len < len(instance['instance_name']):
            max_name_len = len(instance['instance_name'])
        if max_id_len < len(instance['uuid']):
            max_id_len = len(instance['uuid'])
        if max_time_len < len(instance['started_at']):
            max_time_len = len(instance['started_at'])

    print '{0}    {1}    {2}'.format('Name'.center(max_name_len), 'ID'.center(max_id_len), 'Created time'.center(max_time_len))
    print '{0}'.format('-' * (max_name_len + max_id_len + max_time_len + 4 * 2))

    for data in instance_list:
        instance = json.loads(data.details)
        print '{0}    {1}    {2}'.format(str(instance['instance_name']).ljust(max_name_len), str(instance['uuid']).ljust(max_id_len),
                                         str(instance['started_at']).ljust(max_time_len))


def print_organization_ps_output(orgs):
    max_name_len = len('Name')
    max_company_len = len('Company')
    max_time_len = len('Created time')

    for data in orgs:
        org = json.loads(data.details)
        org['company'] = str(org['company']).encode('GBK')
        if max_name_len < len(org['name']):
            max_name_len = len(org['name'])
        if max_time_len < len(org['created_at']):
            max_time_len = len(org['created_at'])
        if max_company_len < len(org['company']):
            max_company_len = len(org['company'])

    print '{0}    {1}    {2}'.format('Name'.center(max_name_len), 'Company'.center(max_company_len), 'Created time'.center(max_time_len))
    print '{0}'.format('-' * (max_name_len + max_company_len + max_time_len + 4 * 2))

    for data in orgs:
        org = json.loads(data.details)
        print '{0}    {1}    {2}'.format(str(org['name']).ljust(max_name_len), str(org['company']).ljust(max_company_len),
                                         str(org['created_at']).ljust(max_time_len))


def print_build_ps_output(builds):
    max_id_len = len('Build id')
    max_client_len = len('Repository type')
    max_repo_len = len('Origin repository path')
    max_tag_len = len('Tag')
    max_state_len = len('State')
    max_time_len = len('Created time')

    for data in builds:
        build = json.loads(data.details)
        print data.details
        if max_id_len < len(build['build_id']):
            max_id_len = len(build['build_id'])
        if max_client_len < len(build['code_repo_client']):
            max_client_len = len(build['code_repo_client'])
        if max_repo_len < len(build['code_repo_path']):
            max_repo_len = len(build['code_repo_path'])
        if max_tag_len < len(build['docker_repo_tag']):
            max_tag_len = len(build['docker_repo_tag'])
        if max_state_len < len(build['status']):
            max_state_len = len(build['status'])
        if max_time_len < len(build['created_at']):
            max_time_len = len(build['created_at'])
    print '{0}    {1}    {2}    {3}    {4}    {5}'.format('Build id'.center(max_id_len), 'Repository type'.center(max_client_len),
                                                          'Origin repository path'.center(max_repo_len), 'Tag'.center(max_tag_len),
                                                          'State'.center(max_state_len), 'Created time'.center(max_time_len))
    print '{}'.format('-' * (max_id_len + max_client_len + max_repo_len + max_tag_len + max_state_len + max_time_len + 4 * 5))

    for data in builds:
        build = json.loads(data.details)
        print '{0}    {1}    {2}    {3}    {4}    {5}'.format(str(build['build_id']).ljust(max_id_len),
                                                              str(build['code_repo_client']).ljust(max_client_len),
                                                              str(build['code_repo_path']).ljust(max_repo_len),
                                                              str(build['docker_repo_tag']).ljust(max_tag_len),
                                                              str(build['status']).ljust(max_state_len),
                                                              str(build['created_at']).ljust(max_time_len))


def print_repo_ps_output(repos):
    max_name_len = len('Name')
    max_type_len = len('Repository type')
    max_auth_len = len('Public/Private')
    max_origin_len = len('Origin repository path')
    max_local_len = len('Local repository path')
    max_time_len = len('Created time')

    for data in repos:
        repo = json.loads(data.details)
        print data.details
        if max_name_len < len(repo['repo_name']):
            max_name_len = len(repo['repo_name'])
        if max_time_len < len(repo['created_at']):
            max_time_len = len(repo['created_at'])
        if max_type_len < len(repo['build_config']['code_repo_client']):
            max_type_len = len(repo['build_config']['code_repo_client'])
        if max_origin_len < len(repo['build_config']['code_repo_path']):
            max_origin_len = len(repo['build_config']['code_repo_path'])
        if max_local_len < len(repo['build_config']['docker_repo_path']):
            max_local_len = len(repo['build_config']['docker_repo_path'])

    print '{0}    {1}    {2}    {3}    {4}    {5}'.format('Name'.center(max_name_len), 'Repository type'.center(max_type_len),
                                                          'Public/Private'.center(max_auth_len), 'Origin repository path'.center(max_origin_len),
                                                          'Local repository path'.center(max_local_len), 'Created time'.center(max_time_len))
    print '{}'.format('-' * (max_name_len + max_type_len + max_auth_len + max_origin_len + max_local_len + max_time_len + 4 * 5))

    for data in repos:
        repo = json.loads(data.details)
        print '{0}    {1}    {2}    {3}    {4}    {5}'.format(str(repo['repo_name']).ljust(max_name_len),
                                                              str(repo['build_config']['code_repo_client']).ljust(max_type_len),
                                                              str('Public' if repo['is_public'] else 'Private').ljust(max_auth_len),
                                                              str(repo['build_config']['code_repo_path']).ljust(max_origin_len),
                                                              str(repo['build_config']['docker_repo_path']).ljust(max_local_len),
                                                              str(repo['created_at']).ljust(max_time_len))


def print_logs(logs):
    entry_list = logs.split('\\r\\n')
    print '[alauda] Logs:'
    for entry in entry_list:
        print entry


def print_json_result(result):
    try:
        print '[alauda] ' + json.dumps(json.loads(result), indent=2)
    except:
        print '[alauda] EMPTY'


def get_flag_pos(src, start_with, end_with, start_pos):
    start_with_pos = src.find(start_with, start_pos)
    if start_with_pos == -1:
        return -1, -1
    end_with_pos = src.find(end_with, start_with_pos + len(end_with))
    if end_with_pos == -1:
        end_with_pos = len(src)
    return start_with_pos, end_with_pos


def valid_repo_info(client, namespace, name, clone_url):
    if client == 'Simple':
        if clone_url is None:
            raise AlaudaInputError('Please specify -ru when -c is Simple')
        return None, None, clone_url

    else:
        if namespace is None or name is None:
            raise AlaudaInputError('Please specify -rns and -rn when -c is GitHub/Bitbucket/OSChina')
        return namespace, name, None


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
        result.append(nodes)
    return result
