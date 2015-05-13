from . import commands


def process_cmds(args):
    if args.cmd == 'login':
        commands.login(args.username, args.password, args.cloud, args.endpoint)
    elif args.cmd == 'logout':
        commands.logout()
    elif args.cmd == 'service':
        if args.subcmd == 'create':
            commands.service_create(image=args.image, name=args.name, start=False, target_num_instances=args.target_num_instances,
                                    instance_size=args.instance_size, run_command=args.run_command, env=args.env, ports=args.expose,
                                    allocation_group=args.allocation_group, volumes=args.volume)
        elif args.subcmd == 'run':
            commands.service_create(image=args.image, name=args.name, start=True, target_num_instances=args.target_num_instances,
                                    instance_size=args.instance_size, run_command=args.run_command, env=args.env, ports=args.expose,
                                    allocation_group=args.allocation_group, volumes=args.volume)
        elif args.subcmd == 'update':
            commands.service_update(args.name, target_num_instances=args.target_num_instances)
        elif args.subcmd == 'inspect':
            commands.service_inspect(args.name)
        elif args.subcmd == 'start':
            commands.service_start(args.name)
        elif args.subcmd == 'stop':
            commands.service_stop(args.name)
        elif args.subcmd == 'rm':
            commands.service_rm(args.name)
        elif args.subcmd == 'ps':
            commands.service_ps()
