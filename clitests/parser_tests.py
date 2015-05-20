import unittest
import mock

from alaudacli import cmd_parser, cmd_processor, util, auth


class UtilTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_image_name_tag(self):
        name, tag = util.parse_image_name_tag('index/user/repo:tag')
        self.assertEqual('index/user/repo', name)
        self.assertEqual('tag', tag)

    def test_parse_image_name_no_tag(self):
        name, tag = util.parse_image_name_tag('index/user/repo')
        self.assertEqual('index/user/repo', name)
        self.assertEqual('latest', tag)

    def test_parse_target_state(self):
        state = util.parse_target_state(True)
        self.assertEqual('STARTED', state)
        state = util.parse_target_state(False)
        self.assertEqual('STOPPED', state)

    def test_parse_instance_ports(self):
        ports = util.parse_instance_ports(['80/tcp', '22'])
        self.assertEqual([{'container_port': 80, 'protocol': 'tcp'}, {'container_port': 22, 'protocol': 'tcp'}], ports)

    def test_parse_envvars(self):
        envvars = util.parse_envvars(['FOO=foo', 'BAR:bar', {'BAZ': 'baz'}, 'A=', 'A= '])
        self.assertEqual({'FOO': 'foo', 'BAR': 'bar', 'BAZ': 'baz', 'A': '', 'A': ' '}, envvars)

    def test_parse_volumes(self):
        volumes = util.parse_volumes(['/var/lib/data1:10', '/var/lib/data2:20'])
        self.assertEqual([{'app_volume_dir': '/var/lib/data1', 'volume_type': 'EBS', 'size_gb': 10},
                          {'app_volume_dir': '/var/lib/data2', 'volume_type': 'EBS', 'size_gb': 20}], volumes)

    def test_build_headers(self):
        headers = auth.build_headers('toooooken')
        self.assertEqual({'Authorization': 'Token toooooken', 'Content-type': 'application/json'}, headers)

    def test_parse_links(self):
        links = util.parse_links(['mysql:db', 'redis:db1'])
        self.assertEqual([('mysql', 'db'), ('redis', 'db1')], links)


class ProcessCmdTest(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_login(self, mock_commands):
        argv = ['login', '-u', 'user', '-p', 'password', '-c', 'io']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.login.assert_called_with('user', 'password', 'io', None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_logout(self, mock_commands):
        argv = ['logout']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.logout.assert_called()

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_create(self, mock_commands):
        argv = ['service', 'create', 'hello', 'index.alauda.io/alauda/hello-world:latest',
                '-t', '2', '-s', 'XS', '-r', '/run.sh',
                '-e', 'FOO=bar', '-p', '5000/tcp', '-ag', 'ag1', '-v', '/var/lib/data1:10', '-l', 'myql:db',
                '-a', '-f', './auto-scaling.cfg', '-n', '']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_create.assert_called_with(image='index.alauda.io/alauda/hello-world:latest',
                                                        name='hello', start=False, target_num_instances=2, instance_size='XS',
                                                        run_command='/run.sh', env=['FOO=bar'], ports=['5000/tcp'], allocation_group='ag1',
                                                        volumes=['/var/lib/data1:10'], links=['myql:db'], scaling_info=(True, './auto-scaling.cfg'),
                                                        namespace='')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_run(self, mock_commands):
        argv = ['service', 'run', 'hello', 'index.alauda.io/alauda/hello-world:latest',
                '-t', '2', '-s', 'XS', '-r', '/run.sh',
                '-e', 'FOO=bar', '-p', '5000/tcp', '-ag', 'ag1', '-v', '/var/lib/data1:10', '-l', 'db',
                '-f', './auto-scaling.cfg', '-n', '']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_create.assert_called_with(image='index.alauda.io/alauda/hello-world:latest',
                                                        name='hello', start=True, target_num_instances=2, instance_size='XS',
                                                        run_command='/run.sh', env=['FOO=bar'], ports=['5000/tcp'], allocation_group='ag1',
                                                        volumes=['/var/lib/data1:10'], links=['db'], scaling_info=(False, './auto-scaling.cfg'),
                                                        namespace='')

#     @mock.patch('alaudacli.cmd_processor.commands')
#     def test_process_service_update(self, mock_commands):
#         argv = ['service', 'update', 'hello', '-t', '2']
#         args = cmd_parser.parse_cmds(argv)
#         cmd_processor.process_cmds(args)
#         mock_commands.service_update.assert_called_with('hello', target_num_instances=2, namespace='', scaling_info=(None, './auto-scaling.cfg'))

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_scale(self, mock_commands):
        argv = ['service', 'scale', 'mysql=2 redis=3']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_scale.assert_called_with(['mysql=2 redis=3'], '')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_enable_autoscale(self, mock_commands):
        argv = ['service', 'enable-autoscaling', 'hello', '-f', 'auto-scaling.cfg']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_enable_autoscale.assert_called_with('hello', '', 'auto-scaling.cfg')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_disable_autoscale(self, mock_commands):
        argv = ['service', 'disable-autoscaling', 'hello', '-t', '2']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_disable_autoscale.assert_called_with('hello', '', 2)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_inspect(self, mock_commands):
        argv = ['service', 'inspect', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_inspect.assert_called_with('hello', namespace='')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_start(self, mock_commands):
        argv = ['service', 'start', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_start.assert_called_with('hello', namespace='')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_stop(self, mock_commands):
        argv = ['service', 'stop', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_stop.assert_called_with('hello', namespace='')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_rm(self, mock_commands):
        argv = ['service', 'rm', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_rm.assert_called_with('hello', namespace='')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_ps(self, mock_commands):
        argv = ['service', 'ps']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_ps.assert_called()

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_compose_up(self, mock_commands):
        argv = ['compose', 'up']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.compose_up.assert_called()
