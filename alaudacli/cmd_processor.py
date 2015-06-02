from . import commands


def process_cmds(args):
    if args.cmd == 'login':
        commands.login(args.username, args.password, args.cloud, args.endpoint)
    elif args.cmd == 'logout':
        commands.logout()
    elif args.cmd == 'service':
        if args.subcmd == 'create':
            commands.service_create(image=args.image, name=args.name, start=False, target_num_instances=args.target_num_instances,
                                    instance_size=args.instance_size, run_command=args.run_command, env=args.env, ports=args.publish,
                                    exposes=args.expose, volumes=args.volume, links=args.link, namespace=args.namespace,
                                    scaling_info=(args.autoscale, args.autoscaling_config), custom_domain_name=args.domain)
        elif args.subcmd == 'run':
            commands.service_create(image=args.image, name=args.name, start=True, target_num_instances=args.target_num_instances,
                                    instance_size=args.instance_size, run_command=args.run_command, env=args.env, ports=args.publish,
                                    exposes=args.expose, volumes=args.volume, links=args.link, namespace=args.namespace,
                                    scaling_info=(args.autoscale, args.autoscaling_config), custom_domain_name=args.domain)
        elif args.subcmd == 'inspect':
            commands.service_inspect(args.name, namespace=args.namespace)
        elif args.subcmd == 'start':
            commands.service_start(args.name, namespace=args.namespace)
        elif args.subcmd == 'stop':
            commands.service_stop(args.name, namespace=args.namespace)
        elif args.subcmd == 'rm':
            commands.service_rm(args.name, namespace=args.namespace)
        elif args.subcmd == 'ps':
            commands.service_ps(namespace=args.namespace, page=args.page)
        elif args.subcmd == 'scale':
            commands.service_scale(args.descriptor, args.namespace)
        elif args.subcmd == 'enable-autoscaling':
            commands.service_enable_autoscaling(args.name, args.namespace, args.autoscaling_config)
        elif args.subcmd == 'disable-autoscaling':
            commands.service_disable_autoscaling(args.name, args.namespace, args.target_num_instances)
        elif args.subcmd == 'logs':
            commands.service_logs(args.name, args.namespace, args.start_time, args.end_time)
        elif args.subcmd == 'instances':
            commands.instance_ps(args.name, namespace=args.namespace)
        elif args.subcmd == 'instance':
            commands.instance_inspect(args.name, args.id, namespace=args.namespace)
        elif args.subcmd == 'instance-logs':
            commands.instance_logs(args.name, args.id, args.namespace, args.start_time, args.end_time)
    elif args.cmd == 'backup':
        if args.subcmd == 'create':
            commands.backup_create(args.name, args.service, args.dir, args.namespace)
        elif args.subcmd == 'list':
            commands.backup_list(args.namespace)
        elif args.subcmd == 'inspect':
            commands.backup_inspect(args.id, args.namespace)
        elif args.subcmd == 'rm':
            commands.backup_rm(args.id, args.namespace)
    elif args.cmd == 'compose':
        if args.subcmd == 'up':
            commands.compose_up(args.file, args.strict)
        elif args.subcmd == 'ps':
            commands.compose_ps(args.file)
        elif args.subcmd == 'start':
            commands.compose_start(args.file, args.strict)
        elif args.subcmd == 'stop':
            commands.compose_stop(args.file)
        elif args.subcmd == 'restart':
            commands.compose_restart(args.file, args.strict)
        elif args.subcmd == 'rm':
            commands.compose_rm(args.file)
        elif args.subcmd == 'scale':
            commands.compose_scale(args.descriptor, args.file)
    elif args.cmd == 'organization':
        if args.subcmd == 'create':
            commands.organization_create(args.name, args.company)
        elif args.subcmd == 'list':
            commands.organization_list()
        elif args.subcmd == 'inspect':
            commands.organization_inspect(args.name)
        elif args.subcmd == 'update':
            commands.organization_update(args.name, args.company)
