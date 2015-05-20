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
    create_parser.add_argument('-p', '--expose', help='Ports to expose, e.g. 5000/tcp', action='append')
    create_parser.add_argument('-ag', '--allocation-group', help='Allocation group', default='')
    create_parser.add_argument('-v', '--volume', help='Volumes, e.g. /var/lib/mysql:10', action='append')
    create_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')
    create_parser.add_argument('-a', '--autoscale', help='Auto scale up/down your services', action='store_true')
    create_parser.add_argument('-f', '--autoscaling_config', help='Auto-scaling config file name', default='./auto-scaling.cfg')

    run_parser = service_subparsers.add_parser('run', help='Create and start a new service', description='Create and start a new service')
    run_parser.add_argument('name', help='Service name')
    run_parser.add_argument('image', help='Docker image used by the service')
    run_parser.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int, default=1)
    run_parser.add_argument('-s', '--instance-size', help='Service container size', choices=['XS', 'S', 'M', 'L', 'XL'], default='XS')
    run_parser.add_argument('-r', '--run-command', help='The command used to start the service containers', default='')
    run_parser.add_argument('-e', '--env', help='Environment variables, e.g. VAR=value', action='append')
    run_parser.add_argument('-l', '--link', help='which service to link.', action='append')
    run_parser.add_argument('-p', '--expose', help='Ports to expose, e.g. 5000/tcp', action='append')
    run_parser.add_argument('-ag', '--allocation-group', help='Allocation group', default='')
    run_parser.add_argument('-v', '--volume', help='volumes.e.g. /var/lib/mysql:10', action='append')
    run_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')
    run_parser.add_argument('-a', '--autoscale', help='Auto scale up/down your services', action='store_true')
    run_parser.add_argument('-f', '--autoscaling_config', help='Auto-scaling config file name', default='./auto-scaling.cfg')

    inspect_parser = service_subparsers.add_parser('inspect', help='Get details of a service', description='Get details of a service')
    inspect_parser.add_argument('name', help='Name of the service to retrieve')
    inspect_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')

    start_parser = service_subparsers.add_parser('start', help='Start a service', description='Start a service')
    start_parser.add_argument('name', help='Name of the service to start')
    start_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')

    stop_parser = service_subparsers.add_parser('stop', help='Stop a service', description='Stop a service')
    stop_parser.add_argument('name', help='Name of the service to stop')
    stop_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')

    rm_parser = service_subparsers.add_parser('rm', help='Remove a service', description='Remove a service')
    rm_parser.add_argument('name', help='Name of the service to remove')
    rm_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')

    ps_parser = service_subparsers.add_parser('ps', help='List services', description='List services')
    ps_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default=None)

    scale_parser = service_subparsers.add_parser('scale', help='Scale a service', description='Scale a service')
    scale_parser.add_argument('descriptor', nargs='*', help='E.g. web=2')
    scale_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')

    enable_autoscaling = service_subparsers.add_parser('enable-autoscaling', help='Auto-scaling a service', description='Auto-scaling a service')
    enable_autoscaling.add_argument('name', help='Name of the service to scale')
    enable_autoscaling.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')
    enable_autoscaling.add_argument('-f', '--autoscaling_config', help='Auto-scaling config file name', default='./auto-scaling.cfg')

    disable_autoscaling = service_subparsers.add_parser('disable-autoscaling', help='Manual-scaling a service', description='Manual-scaling a service')
    disable_autoscaling.add_argument('name', help='Name of the service to scale')
    disable_autoscaling.add_argument('-n', '--namespace', help='Namespace which service belongs to', default='')
    disable_autoscaling.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int)


def _add_backups_parser(subparsers):
    backups_parser = subparsers.add_parser('backup', help='Backup operations', description='Backup operations')
    backup_subparsers = backups_parser.add_subparsers(title='Alauda backup commands', dest='subcmd')

    create_parser = backup_subparsers.add_parser('create', help='Create a new backup', description='Create a new backup')
    create_parser.add_argument('service_name', help='Name of the service to create backup')
    create_parser.add_argument('mounted_dir', help='directory of the service mounted')
    create_parser.add_argument('snapshot_name', help='backup name')
    create_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default=None)

    list_parser = backup_subparsers.add_parser('list', help='list backups', description='list backups')
    list_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default=None)

    inspect_parser = backup_subparsers.add_parser('inspect', help='Get details of a backup', description='Get details of a backup')
    inspect_parser.add_argument('id', help='uuid of the backup')
    inspect_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default=None)

    rm_parser = backup_subparsers.add_parser('rm', help='Remove a backup', description='Remove a backup')
    rm_parser.add_argument('id', help='uuid of the backup')
    rm_parser.add_argument('-n', '--namespace', help='Namespace which service belongs to', default=None)


def _add_compose_parser(subparsers):
    compose_parser = subparsers.add_parser('compose', help='Compose multi-container app', description='Compose multi-container app')
    compose_subparsers = compose_parser.add_subparsers(title='Alauda compose commands', dest='subcmd')

    up_parser = compose_subparsers.add_parser('up', help='Create and start all service containers', description='Create and start all service containers')
    up_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    ps_parser = compose_subparsers.add_parser('ps', help='List containers', description='Lists container')
    ps_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    start_parser = compose_subparsers.add_parser('start', help='Start all service containers', description='Start all service containers')
    start_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    stop_parser = compose_subparsers.add_parser('stop', help='Stop all service containers', description='Stop all service containers')
    stop_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    restart_parser = compose_subparsers.add_parser('restart', help='Restart all service containers', description='Restart all service containers')
    restart_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    rm_parser = compose_subparsers.add_parser('rm', help='Remove all service containers', description='Remove all service containers')
    rm_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    scale_parser = compose_subparsers.add_parser(
        'scale',
        help='Set number of containers to run for a service',
        description='Set number of containers to run for a service')
    scale_parser.add_argument('descriptor', nargs='*', help='E.g. web=2 db=1')
    scale_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
