import getpass
import json
import requests

import util
import auth
import compose
from service import Service
from backup import Backup


def login(username, password, cloud, endpoint):
    if not username:
        username = raw_input('Username: ')
    if not password:
        password = getpass.getpass()

    api_endpoint = endpoint
    if api_endpoint is None:
        api_endpoint = auth.get_api_endpoint(cloud)
    url = api_endpoint + 'generate-api-token/'
    payload = {'username': username, 'password': password}
    r = requests.post(url, payload)
    d = json.loads(r.text)
    token = d['token']
    auth.save_token(api_endpoint, token, username)
    print '[alauda] Successfully logged in as {}.'.format(username)


def logout():
    auth.delete_token()
    print '[alauda] Bye'


def service_create(image, name, start, target_num_instances, instance_size, run_command, env, ports,
                   allocation_group, volumes, links, namespace, scaling_info, custom_domain_name):
    image_name, image_tag = util.parse_image_name_tag(image)
    instance_ports = util.parse_instance_ports(ports)
    instance_envvars = util.parse_envvars(env)
    links = util.parse_links(links)
    volumes = util.parse_volumes(volumes)
    scaling_mode, scaling_cfg = util.parse_autoscale_info(scaling_info)
    if scaling_mode is None:
        scaling_mode = 'MANUAL'
    service = Service(name=name,
                      image_name=image_name,
                      image_tag=image_tag,
                      target_num_instances=target_num_instances,
                      instance_size=instance_size,
                      run_command=run_command,
                      instance_ports=instance_ports,
                      instance_envvars=instance_envvars,
                      allocation_group=allocation_group,
                      volumes=volumes,
                      links=links,
                      namespace=namespace,
                      scaling_mode=scaling_mode,
                      autoscaling_config=scaling_cfg,
                      custom_domain_name=custom_domain_name)
    if start:
        service.run()
    else:
        service.create()


def service_inspect(name, namespace):
    service = Service.fetch(name, namespace)
    result = service.inspect()
    print '[alauda] ' + json.dumps(json.loads(result), indent=2)


def service_start(name, namespace):
    service = Service.fetch(name, namespace)
    service.start()


def service_stop(name, namespace):
    service = Service.fetch(name, namespace)
    service.stop()


def service_rm(name, namespace):
    Service.remove(name, namespace)


def service_ps(namespace):
    service_list = Service.list(namespace)
    util.print_ps_output(service_list)


def service_scale(descriptor, namespace):
    scale_dict = util.parse_scale(descriptor)
    for service_name, service_num in scale_dict.items():
        service = Service.fetch(service_name, namespace)
        service.scale(service_num)


def service_enable_autoscaling(name, namespace, autoscaling_config):
    _, scaling_cfg = util.parse_autoscale_info(('AUTO', autoscaling_config))
    service = Service.fetch(name, namespace)
    service.enable_autoscaling(scaling_cfg)


def service_disable_autoscaling(name, namespace, target_num_instances):
    service = Service.fetch(name, namespace)
    service.disable_autoscaling(target_num_instances)


def service_logs(name, namespace, start_time, end_time):
    service = Service.fetch(name, namespace)
    result = service.logs(start_time, end_time)
    print "{}".format(result)


def compose_up(file):
    project = compose.load_project(file)
    project.up()


def compose_ps(file):
    project = compose.load_project(file)
    project.ps()


def compose_start(file):
    project = compose.load_project(file)
    project.start()


def compose_stop(file):
    project = compose.load_project(file)
    project.stop()


def compose_restart(file):
    project = compose.load_project(file)
    project.restart()


def compose_rm(file):
    project = compose.load_project(file)
    project.rm()


def compose_scale(descriptor, file):
    project = compose.load_project(file)
    scale_dict = util.parse_scale(descriptor)
    project.scale(scale_dict)


def backup_create(name, service_name, mounted_dir, namespace):
    service = Service.fetch(service_name, namespace)
    backup = Backup(service=service, name=name, mounted_dir=mounted_dir)
    backup.create()


def backup_list(namespace):
    backup_list = Backup.list(namespace)
    util.print_backup_ps_output(backup_list)


def backup_inspect(id, namespace):
    backup = Backup.fetch(id, namespace)
    result = backup.inspect()
    print '[alauda] ' + json.dumps(json.loads(result), indent=2)


def backup_rm(id, namespace):
    Backup.remove(id, namespace)
