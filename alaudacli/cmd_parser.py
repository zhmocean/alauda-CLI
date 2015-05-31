import argparse

from alaudacli import __version__


def parse_cmds(argv):
    parser = create_parser()
    args = parser.parse_args(argv)
    return args


def create_parser():
    parser = argparse.ArgumentParser(description="Alauda CLI", prog='alauda')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    subparsers = parser.add_subparsers(title="Alauda CLI commands", dest='cmd')
    _add_login_parser(subparsers)
    _add_logout_parser(subparsers)
    _add_service_parser(subparsers)
    _add_compose_parser(subparsers)
    _add_backups_parser(subparsers)
    _add_organization_parser(subparsers)
    _add_repository_parser(subparsers)
    _add_build_parser(subparsers)
    return parser


def _add_login_parser(subparsers):
    login_parser = subparsers.add_parser('login', help='Alauda login', description='Alauda login')
    login_parser.add_argument('-u', '--username', help='Alauda username')
    login_parser.add_argument('-p', '--password', help='Alauda password')
    login_parser.add_argument('-c', '--cloud', help='Alauda Cloud to connect to', choices={'cn', 'io'}, default='cn')
    login_parser.add_argument('-e', '--endpoint', help='Alauda API endpoint to use')


def _add_logout_parser(subparsers):
    subparsers.add_parser('logout', help='Log out', description='Log out')


def _add_service_parser(subparsers):
    service_parser = subparsers.add_parser('service', help='Service operations', description='Service operations')
    service_subparsers = service_parser.add_subparsers(title='Alauda service commands', dest='subcmd')

    create_parser = service_subparsers.add_parser('create', help='Create a new service', description='Create a new service')
    create_parser.add_argument('name', help='Service name')
    create_parser.add_argument('image', help='Docker image used by the service')
    create_parser.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int, default=1)
    create_parser.add_argument('-s', '--instance-size', help='Service container size', choices=['XS', 'S', 'M', 'L', 'XL'], default='XS')
    create_parser.add_argument('-r', '--run-command', help='The command used to start the service containers', default='')
    create_parser.add_argument('-e', '--env', help='Environment variables, e.g. VAR=value', action='append')
    create_parser.add_argument('-l', '--link', help='which service to link.', action='append')
    create_parser.add_argument('-p', '--publish', help='Ports to publish, e.g. 5000/tcp', action='append')
    create_parser.add_argument('-v', '--volume', help='Volumes, e.g. /var/lib/mysql:10', action='append')
    create_parser.add_argument('-n', '--namespace', help='Service namespace')
    create_parser.add_argument('-a', '--autoscale', help='Enable auto-scaling', action='store_true')
    create_parser.add_argument('-f', '--autoscaling-config', help='Auto-scaling config file name', default='./auto-scaling.cfg')
    create_parser.add_argument('-d', '--domain', help='Custom domain name')

    run_parser = service_subparsers.add_parser('run', help='Create and start a new service', description='Create and start a new service')
    run_parser.add_argument('name', help='Service name')
    run_parser.add_argument('image', help='Docker image used by the service')
    run_parser.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int, default=1)
    run_parser.add_argument('-s', '--instance-size', help='Service container size', choices=['XS', 'S', 'M', 'L', 'XL'], default='XS')
    run_parser.add_argument('-r', '--run-command', help='The command used to start the service containers', default='')
    run_parser.add_argument('-e', '--env', help='Environment variables, e.g. VAR=value', action='append')
    run_parser.add_argument('-l', '--link', help='which service to link.', action='append')
    run_parser.add_argument('-p', '--publish', help='Ports to publish, e.g. 5000/tcp', action='append')
    run_parser.add_argument('-v', '--volume', help='volumes.e.g. /var/lib/mysql:10', action='append')
    run_parser.add_argument('-n', '--namespace', help='Service namespace')
    run_parser.add_argument('-a', '--autoscale', help='Enable auto-scaling', action='store_true')
    run_parser.add_argument('-f', '--autoscaling-config', help='Auto-scaling config file name', default='./auto-scaling.cfg')
    run_parser.add_argument('-d', '--domain', help='Custom domain name')

    inspect_parser = service_subparsers.add_parser('inspect', help='Get details of a service', description='Get details of a service')
    inspect_parser.add_argument('name', help='Name of the service to retrieve')
    inspect_parser.add_argument('-n', '--namespace', help='Service namespace')

    start_parser = service_subparsers.add_parser('start', help='Start a service', description='Start a service')
    start_parser.add_argument('name', help='Name of the service to start')
    start_parser.add_argument('-n', '--namespace', help='Service namespace')

    stop_parser = service_subparsers.add_parser('stop', help='Stop a service', description='Stop a service')
    stop_parser.add_argument('name', help='Name of the service to stop')
    stop_parser.add_argument('-n', '--namespace', help='Service namespace')

    rm_parser = service_subparsers.add_parser('rm', help='Remove a service', description='Remove a service')
    rm_parser.add_argument('name', help='Name of the service to remove')
    rm_parser.add_argument('-n', '--namespace', help='Service namespace')

    ps_parser = service_subparsers.add_parser('ps', help='List services', description='List services')
    ps_parser.add_argument('-n', '--namespace', help='Service namespace')
    ps_parser.add_argument('-p', '--page', help='Page number', default=1)

    scale_parser = service_subparsers.add_parser('scale', help='Scale a service', description='Scale a service')
    scale_parser.add_argument('descriptor', nargs='*', help='E.g. web=2')
    scale_parser.add_argument('-n', '--namespace', help='Service namespace')

    enable_autoscaling_parser = service_subparsers.add_parser('enable-autoscaling', help='Enable auto-scaling', description='Enable auto-scaling')
    enable_autoscaling_parser.add_argument('name', help='Service name')
    enable_autoscaling_parser.add_argument('-n', '--namespace', help='Service namespace')
    enable_autoscaling_parser.add_argument('-f', '--autoscaling-config', help='Auto-scaling config file name', default='./auto-scaling.cfg')

    disable_autoscaling_parser = service_subparsers.add_parser('disable-autoscaling', help='Disable auto-scaling', description='Disable auto-scaling')
    disable_autoscaling_parser.add_argument('name', help='Service name')
    disable_autoscaling_parser.add_argument('-n', '--namespace', help='Service namespace')
    disable_autoscaling_parser.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int)

    logs_parser = service_subparsers.add_parser('logs', help='Query service log', description='Query service log')
    logs_parser.add_argument('name', help='Service name')
    logs_parser.add_argument('-n', '--namespace', help='Service namespace')
    logs_parser.add_argument('-s', '--start-time', help='Logs query start time. e.g. 2015-05-01 12:12:12')
    logs_parser.add_argument('-e', '--end-time', help='Logs query end time. e.g. 2015-05-01 12:12:12')

    list_instance_parser = service_subparsers.add_parser('instances', help='List instances', description='List instances')
    list_instance_parser.add_argument('name', help='Service name')
    list_instance_parser.add_argument('-n', '--namespace', help='Service namespace')

    inspect_instance_parser = service_subparsers.add_parser('instance', help='Get details of a instance', description='Get details of a instance')
    inspect_instance_parser.add_argument('name', help='Service name')
    inspect_instance_parser.add_argument('id', help='Instance uuid')
    inspect_instance_parser.add_argument('-n', '--namespace', help='Service namespace')

    logs_instance_parser = service_subparsers.add_parser('instance-logs', help='Query instance log', description='Query instance log')
    logs_instance_parser.add_argument('name', help='Service name')
    logs_instance_parser.add_argument('id', help='Instance uuid')
    logs_instance_parser.add_argument('-s', '--start-time', help='Logs query start time. e.g. 2015-05-01 12:12:12')
    logs_instance_parser.add_argument('-e', '--end-time', help='Logs query end time. e.g. 2015-05-01 12:12:12')
    logs_instance_parser.add_argument('-n', '--namespace', help='Service namespace')


def _add_backups_parser(subparsers):
    backups_parser = subparsers.add_parser('backup', help='Backup operations', description='Backup operations')
    backup_subparsers = backups_parser.add_subparsers(title='Alauda backup commands', dest='subcmd')

    create_parser = backup_subparsers.add_parser('create', help='Create a new volume backup', description='Create a new volume backup')
    create_parser.add_argument('name', help='Backup name')
    create_parser.add_argument('service', help='Name of the service to create volume backup for')
    create_parser.add_argument('dir', help='Mounted volume directory to backup')
    create_parser.add_argument('-n', '--namespace', help='Service namespace')

    list_parser = backup_subparsers.add_parser('list', help='List volume backups', description='list volume backups')
    list_parser.add_argument('-n', '--namespace', help='Service namespace')

    inspect_parser = backup_subparsers.add_parser('inspect', help='Get details of a volume backup', description='Get details of a volume backup')
    inspect_parser.add_argument('id', help='UUID of the volume backup')
    inspect_parser.add_argument('-n', '--namespace', help='Service namespace')

    rm_parser = backup_subparsers.add_parser('rm', help='Remove a volume backup', description='Remove a volume backup')
    rm_parser.add_argument('id', help='UUID of the volume backup')
    rm_parser.add_argument('-n', '--namespace', help='Service namespace')


def _add_compose_parser(subparsers):
    compose_parser = subparsers.add_parser('compose', help='Compose multi-container app', description='Compose multi-container app')
    compose_subparsers = compose_parser.add_subparsers(title='Alauda compose commands', dest='subcmd')

    up_parser = compose_subparsers.add_parser('up', help='Create and start all service containers', description='Create and start all service containers')
    up_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    up_parser.add_argument('-s', '--strict', help='Strict mode', action='store_true')

    ps_parser = compose_subparsers.add_parser('ps', help='List containers', description='Lists container')
    ps_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    start_parser = compose_subparsers.add_parser('start', help='Start all service containers', description='Start all service containers')
    start_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    start_parser.add_argument('-s', '--strict', help='Strict mode', action='store_true')

    stop_parser = compose_subparsers.add_parser('stop', help='Stop all service containers', description='Stop all service containers')
    stop_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    restart_parser = compose_subparsers.add_parser('restart', help='Restart all service containers', description='Restart all service containers')
    restart_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    restart_parser.add_argument('-s', '--strict', help='Strict mode', action='store_true')

    rm_parser = compose_subparsers.add_parser('rm', help='Remove all service containers', description='Remove all service containers')
    rm_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    scale_parser = compose_subparsers.add_parser(
        'scale',
        help='Set number of containers to run for a service',
        description='Set number of containers to run for a service')
    scale_parser.add_argument('descriptor', nargs='*', help='E.g. web=2 db=1')
    scale_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')


def _add_organization_parser(subparsers):
    org_parser = subparsers.add_parser('organization', help='Organization operations', description='Organization operations')
    org_subparsers = org_parser.add_subparsers(title='Alauda organization commands', dest='subcmd')

    org_subparsers.add_parser('list', help='List all organization', description='List all organization')

    create_parser = org_subparsers.add_parser('create', help='Create a new organization', description='Create a new organization')
    create_parser.add_argument('name', help='Organization name')
    create_parser.add_argument('company', help='Company name')

    inspect_parser = org_subparsers.add_parser('inspect', help='Get details of an organization', description='Get details of an organization')
    inspect_parser.add_argument('name', help='Organization name')

    update_parser = org_subparsers.add_parser('update', help='Update an exist orgnization', description='Update an exist orgnization')
    update_parser.add_argument('name', help='Organization name')
    update_parser.add_argument('company', help='Company name')


def _add_repository_parser(subparsers):
    repo_parser = subparsers.add_parser('repository', help='Repository operations', description='Repository operations')
    repo_subparsers = repo_parser.add_subparsers(title='Alauda repository commands', dest='subcmd')

    create_parser = repo_subparsers.add_parser('create', help='Create a new repository', description='Create a new repository')
    create_parser.add_argument('name', help='Repository name')
    create_parser.add_argument('-d', '--description', help='Repository brief', default='docker images')
    create_parser.add_argument('-fd', '--full-description', help='Repository full description', default='')
    create_parser.add_argument('-p', '--public', help='Public repository or not', action='store_true')
    create_parser.add_argument('-c', '--client', help='Repository client', choices=['Simple', 'GitHub', 'Bitbucket', 'OSChina'], default='Simple')
    create_parser.add_argument('-rns', '--repo-namespace', help='Origin repository namespace')
    create_parser.add_argument('-rn', '--repo-name', help='Origin repository name')
    create_parser.add_argument('-ru', '--repo-clone-url', help='Origin repository url')
    create_parser.add_argument('-f', '--tag-config-file', help='Tag config file', default='./create_repo_config.example')
    create_parser.add_argument('-n', '--namespace', help='Repository namespace')

    list_parser = repo_subparsers.add_parser('list', help='List all repositories', description='List all repositories')
    list_parser.add_argument('-n', '--namespace', help='Repository namespace')
    list_parser.add_argument('-p', '--page', help='Page number', default=1)

    inspect_parser = repo_subparsers.add_parser('inspect', help='Get detail of a repository', description='Get detail of a repository')
    inspect_parser.add_argument('name', help='Repository name')
    inspect_parser.add_argument('-n', '--namespace', help='Repository namespace')

    update_parser = repo_subparsers.add_parser('update', help='Update a repository', description='Update a repository')
    update_parser.add_argument('name', help='Repository name')
    update_parser.add_argument('-d', '--description', help='Repository brief')
    update_parser.add_argument('-fd', '--full-description', help='Repository full description')
    update_parser.add_argument('-n', '--namespace', help='Repository namespace')

    public_parser = repo_subparsers.add_parser('public', help='Make a repository to public', description='Make a repository to public')
    public_parser.add_argument('name', help='Repository name')
    public_parser.add_argument('-n', '--namespace', help='Repository namespace')

    private_parser = repo_subparsers.add_parser('private', help='Make a repository to private', description='Make a repository to private')
    private_parser.add_argument('name', help='Repository name')
    private_parser.add_argument('-n', '--namespace', help='Repository namespace')

    rm_parser = repo_subparsers.add_parser('rm', help='Delete a repository', description='Delete a repository')
    rm_parser.add_argument('name', help='Repository name')
    rm_parser.add_argument('-n', '--namespace', help='Repository namespace')

    tags_parser = repo_subparsers.add_parser('tags', help='List tags', description='List tags')
    tags_parser.add_argument('name', help='Repository name')
    tags_parser.add_argument('-n', '--namespace', help='Repository namespace')

    tag_parser = repo_subparsers.add_parser('tag', help='Get detail of a tag', description='Get detail of a tag')
    tag_parser.add_argument('name', help='Repository name')
    tag_parser.add_argument('tag_name', help='Tag name')
    tag_parser.add_argument('-n', '--namespace', help='Repository namespace')

    update_tag_parser = repo_subparsers.add_parser('tag-update', help='Update repository tag config', description='Update repository tag config')
    update_tag_parser.add_argument('name', help='Repository name')
    update_tag_parser.add_argument('-f', '--tag-config-file', help='Tag config file', default='./update_repo_config.example')
    update_tag_parser.add_argument('-n', '--namespace', help='Repository namespace')


def _add_build_parser(subparsers):
    build_parser = subparsers.add_parser('build', help='Build operations', description='Build operations')
    build_subparsers = build_parser.add_subparsers(title='Alauda build commands', dest='subcmd')

    trigger_parser = build_subparsers.add_parser('trigger', help='Trigger a build', description='Trigger a build')
    trigger_parser.add_argument('name', help='Repository name')
    trigger_parser.add_argument('-n', '--namespace', help='Repository namespace')
    trigger_parser.add_argument('-t', '--tag', help='Tag name', default='latest')

    list_parser = build_subparsers.add_parser('list', help='List all builds', description='List all builds')
    list_parser.add_argument('-p', '--page', help='Page number', default=1)

    inspect_parser = build_subparsers.add_parser('inspect', help='Get detail of a build', description='Get detail of a build')
    inspect_parser.add_argument('id', help='Build id')

    rm_parser = build_subparsers.add_parser('rm', help='Delete a build', description='Delete a build')
    rm_parser.add_argument('id', help='Build id')

    logs_parser = build_subparsers.add_parser('logs', help='Query a build log', description='Query a build log')
    logs_parser.add_argument('id', help='Build id')
    logs_parser.add_argument('-s', '--start-time', help='Logs query start time. e.g. 2015-05-01 12:12:12')
    logs_parser.add_argument('-e', '--end-time', help='Logs query end time. e.g. 2015-05-01 12:12:12')
