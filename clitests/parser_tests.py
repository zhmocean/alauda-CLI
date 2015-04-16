import unittest
import mock

from alaudacli import cmd_parser, cmd_processor


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
        argv = ['service', 'create', 'index.alauda.io/alauda/hello-world:latest',
                '-n', 'hello', '--start', '-t', '2', '-s', 'XS', '-r', '/run.sh',
                '-e', 'FOO=bar', '-p', '5000/tcp']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_create.assert_called_with(image='index.alauda.io/alauda/hello-world:latest',
                                                        name='hello', start=True, target_num_instances=2, instance_size='XS',
                                                        run_command='/run.sh', env=['FOO=bar'], ports=['5000/tcp'])

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_update(self, mock_commands):
        argv = ['service', 'update', 'hello', '-t', '2']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_update.assert_called_with('hello', target_num_instances=2)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_get(self, mock_commands):
        argv = ['service', 'get', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_get.assert_called_with('hello')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_start(self, mock_commands):
        argv = ['service', 'start', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_start.assert_called_with('hello')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_stop(self, mock_commands):
        argv = ['service', 'stop', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_stop.assert_called_with('hello')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_delete(self, mock_commands):
        argv = ['service', 'delete', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_delete.assert_called_with('hello')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_list(self, mock_commands):
        argv = ['service', 'list']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_list.assert_called_()
