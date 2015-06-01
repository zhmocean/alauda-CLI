# Alauda Command Line

显示所有支持的命令，执行`alauda`或者`alauda -h`:

```
bash-3.2# alauda
usage: alauda [-h] [-v] {login,logout,service,compose,backup,organization} ...

Alauda CLI

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Alauda CLI commands:
  {login,logout,service,compose,backup,organization}
    login               Alauda login
    logout              Log out
    service             Service operations
    compose             Compose multi-container app
    backup              Backup operations
    organization        Organization operations
```

使用`-v`来查看当前alauda CLI版本

```
bash-3.2# alauda -v
alauda 0.1.0

```
在下面所有的参数说明中:

* `-e[]`表示可以指明多次。

	例如:`-e DB_NAME=mysql -e DB_PASSOWRD=123`

* `-d=""` 表示值是字符串。

	例如:`-d "www.myself-domain.com"`

* `-s={XS,S,M,L,XL}` 表示必须是所给定的值之一。

	例如: `-s XL`

* `-t=1` 表示所给定的值必须为数字

	例如: `-t=1`

* `-a=false` 表示不输出此参数的情况下，参数的值false，如果显示的列出该参数，则表明改参数的值为true。

## Help

显示任何支持命令的帮助信息，只需要在命令后面增加参数`-h`

```
bash-3.2# alauda service create -h
usage: alauda service create [-h] [-t TARGET_NUM_INSTANCES] [-s {XS,S,M,L,XL}]
                             [-r RUN_COMMAND] [-e ENV] [-l LINK] [-p PUBLISH]
                             [-v VOLUME] [-n NAMESPACE] [-a]
                             [-f AUTOSCALING_CONFIG] [-d DOMAIN]
                             name image

Create a new service

positional arguments:
  name                  Service name
  image                 Docker image used by the service

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_NUM_INSTANCES, --target-num-instances TARGET_NUM_INSTANCES
                        Target number of instances for the service
  -s {XS,S,M,L,XL}, --instance-size {XS,S,M,L,XL}
                        Service container size
  -r RUN_COMMAND, --run-command RUN_COMMAND
                        The command used to start the service containers
  -e ENV, --env ENV     Environment variables, e.g. VAR=value
  -l LINK, --link LINK  which service to link.
  -p PUBLISH, --publish PUBLISH
                        Ports to publish, e.g. 5000/tcp
  -v VOLUME, --volume VOLUME
                        Volumes, e.g. /var/lib/mysql:10
  -n NAMESPACE, --namespace NAMESPACE
                        Service namespace
  -a, --autoscale       Enable auto-scaling
  -f AUTOSCALING_CONFIG, --autoscaling-config AUTOSCALING_CONFIG
                        Auto-scaling config file name
  -d DOMAIN, --domain DOMAIN
                        Custom domain name
```

## Login

Login命令是用于登录灵雀云美国区或者中国区系统。`-c`选项可以简单的指明所登陆的系统。`cn`为中国区，`io`为美国区。当然，你也可以使用`-e`参数来显示的指明需要登陆的地址，例如:`https://api.alauda.io/v1/`

```
usage: alauda login [-h] [-u USERNAME] [-p PASSWORD] [-c {cn,io}]
                    [-e ENDPOINT]

Alauda login

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Alauda username
  -p PASSWORD, --password PASSWORD
                        Alauda password
  -c {cn,io}, --cloud {cn,io}
                        Alauda Cloud to connect to
  -e ENDPOINT, --endpoint ENDPOINT
                        Alauda API endpoint to use
```

样例:

```
bash-3.2# alauda login -c cn -u test -p test
[alauda] Successfully logged in as test.
[alauda] OK

bash-3.2# alauda login -e https://api.alauda.io/v1/ -u test -p test
[alauda] Successfully logged in as test.
[alauda] OK
```

## Logout

退出登陆。

```
usage: alauda logout [-h]

Log out

optional arguments:
  -h, --help  show this help message and exit
```


样例:

```
bash-3.2# alauda logout
[alauda] Bye
[alauda] OK

```

## Service

用于在已登录的系统上创建服务。

```
usage: alauda service [-h]

                      {create,run,inspect,start,stop,rm,ps,scale,enable-autoscaling,disable-autoscaling,logs,instances,instance,instance-logs,instance-metrics}
                      ...

Service operations

optional arguments:
  -h, --help            show this help message and exit

Alauda service commands:
  {create,run,inspect,start,stop,rm,ps,scale,enable-autoscaling,disable-autoscaling,logs,instances,instance,instance-logs,instance-metrics}
    create              Create a new service
    run                 Create and start a new service
    inspect             Get details of a service
    start               Start a service
    stop                Stop a service
    rm                  Remove a service
    ps                  List services
    scale               Scale a service
    enable-autoscaling  Enable auto-scaling
    disable-autoscaling Disable auto-scaling
    logs                Query service log
    instances           List instances
    instance            Get details of a instance
    instance-logs       Query instance log
```

样例:

```
bash-3.2# alauda run hello index.alauda.cn/alauda/hello-world:latest -p 80
[alauda] Creating and starting service "hello"
[alauda] OK

```

###create

用于创建一个服务(只创建，不运行)。并通过参数指明服务的名称，所用镜像名称，以及服务所需容器大小，容器数量等信息。

```
usage: alauda service create [-h] [-t TARGET_NUM_INSTANCES] [-s {XS,S,M,L,XL}]
                             [-r RUN_COMMAND] [-e ENV] [-l LINK] [-p PUBLISH]
                             [-ex EXPOSE] [-v VOLUME] [-n NAMESPACE] [-a]
                             [-f AUTOSCALING_CONFIG] [-d DOMAIN]
                             name image

Create a new service

positional arguments:
  name                  Service name
  image                 Docker image used by the service

optional arguments:
  -h, --help            				show this help message and exit
  -t, --target-num-instances＝1			Target number of instances for the service
  -s, --instance-size={XS,S,M,L,XL}	Service container size
  -r, --run-command=""					The command used to start the service containers
  -e, --env=[]     						Environment variables, e.g. VAR=value
  -l, --link=[]  						which service to link.
  -p, --publish=[]						Ports to publish, e.g. 5000/tcp
  -ex, --expose=[]						Internal ports, e.g. 5000
  -v, --volume=[]						Volumes, e.g. /var/lib/mysql:10
  -n, --namespace=""					Service namespace
  -a, --autoscale=false			        Enable auto-scaling
  -f, --autoscaling-config=""			Auto-scaling config file name
  -d, --domain=""						Custom domain name
```

* 如果显示的指明了`-a` 参数，则表明讲服务设置为自动调节模式，此模式下需要使用`-f` 来指明自动调节参数配置文件所在路径。

###run

用于创建并执行一个服务。并通过参数指明服务的名称，所用镜像名称，以及服务所需容器大小，容器数量等信息。

```
usage: alauda service run [-h] [-t TARGET_NUM_INSTANCES] [-s {XS,S,M,L,XL}]
                          [-r RUN_COMMAND] [-e ENV] [-l LINK] [-p PUBLISH]
                          [-ex EXPOSE] [-v VOLUME] [-n NAMESPACE] [-a]
                          [-f AUTOSCALING_CONFIG] [-d DOMAIN]
                          name image

Create and start a new service

positional arguments:
  name                  Service name
  image                 Docker image used by the service

optional arguments:
  -h, --help            				show this help message and exit
  -t, --target-num-instances＝1			Target number of instances for the service
  -s, --instance-size={XS,S,M,L,XL}	Service container size
  -r, --run-command=""					The command used to start the service containers
  -e, --env=[]     						Environment variables, e.g. VAR=value
  -l, --link=[]  						which service to link.
  -p, --publish=[]						Ports to publish, e.g. 5000/tcp
  -ex, --expose=[]						Internal ports, e.g. 5000
  -v, --volume=[]						Volumes, e.g. /var/lib/mysql:10
  -n, --namespace=""					Service namespace
  -a, --autoscale=false			        Enable auto-scaling
  -f, --autoscaling-config=""			Auto-scaling config file name
  -d, --domain=""						Custom domain name
```

###inspect

获取一个服务的详细信息。

```
usage: alauda service inspect [-h] [-n NAMESPACE] name

Get details of a service

positional arguments:
  name                  Name of the service to retrieve

optional arguments:
  -h, --help            	show this help message and exit
  -n, --namespace=""		Service namespace
```

### start

启动一个处于暂停状态的服务

```
usage: alauda service start [-h] [-n NAMESPACE] name

Start a service

positional arguments:
  name                  Name of the service to start

optional arguments:
  -h, --help            	show this help message and exit
  -n, --namespace=""		Service namespace
```

###stop

启动一个处于运行状态的服务

```
usage: alauda service stop [-h] [-n NAMESPACE] name

Stop a service

positional arguments:
  name                  Name of the service to stop

optional arguments:
  -h, --help            	show this help message and exit
  -n, --namespace=""		Service namespace
```

###rm

删除一个已存在的服务

```
usage: alauda service rm [-h] [-n NAMESPACE] name

Remove a service

positional arguments:
  name                  Name of the service to remove

optional arguments:
  -h, --help            	show this help message and exit
  -n, --namespace=""		Service namespace
```

###ps

列出当前账户下所有的服务

###scale

调节当前服务中实例适量

```
usage: alauda service scale [-h] [-n NAMESPACE] [descriptor [descriptor ...]]

Scale a service

positional arguments:
  descriptor            E.g. web=2

optional arguments:
  -h, --help            	show this help message and exit
  -n, --namespace=""		Service namespace
```

###enable-autoscaling

将当前服务的状态设置为自动调节模式

```
usage: alauda service enable-autoscaling [-h] [-n NAMESPACE]
                                         [-f AUTOSCALING_CONFIG]
                                         name

Enable auto-scaling

positional arguments:
  name                  Service name

optional arguments:
  -h, --help            			show this help message and exit
  -n, --namespace=""				Service namespace
  -f, --autoscaling-config=""		Auto-scaling config file name
```
必须显示指明自动调节配置文件所在位置，如果不指明，则默认当前路径下的`auto-scaling.example`文件为配置文件。

###disable-autoscaling

将当前服务的状态设置为人工调节模式

```
usage: alauda service disable-autoscaling [-h] [-n NAMESPACE]
                                          [-t TARGET_NUM_INSTANCES]
                                          name

Disable auto-scaling

positional arguments:
  name                  Service name

optional arguments:
  -h, --help            		show this help message and exit
  -n, --namespace=""			Service namespace
  -t, --target-num-instances=1	Target number of instances for the service
```
设置为人工模式的同时，可以使用`-t`指定服务的实例数量，如果不指定，则以自动调节模式的最后实例数量为当前服务的实例数量。

###logs

查看当前服务的日志信息

```
usage: alauda service logs [-h] [-n NAMESPACE] [-s START_TIME] [-e END_TIME]
                           name

Query service log

positional arguments:
  name                  Service name

optional arguments:
  -h, --help            		show this help message and exit
  -n, --namespace=""			Service namespace
  -s, --start-time=""			Logs query start time. e.g. 2015-05-01 12:12:12
  -e, --end-time=""				Logs query end time. e.g. 2015-05-01 12:12:12
```
如果不指定起始和终止时间，那么返回最近一小时以内的日志。如果仅指定起始时间，那么返回给定的起始时间到当前时间的日志，如果只给定终止时间，那么返回终止时间之前一小时以内的日志。

###instances

列出服务所有的实例

```
usage: alauda service instances [-h] [-n NAMESPACE] name

List instances

positional arguments:
  name                  Service name

optional arguments:
  -h, --help            	show this help message and exit
  -n, --namespace=""		Service namespace
```

###instance

查看某一个实例的详细信息

```
Get details of a instance

positional arguments:
  name                  Service name
  id                    Instance uuid

optional arguments:
  -h, --help            	show this help message and exit
  -n, --namespace=""		Service namespace
```

###instance-logs

查看某一实例的日志信息

```
usage: alauda service instance-logs [-h] [-s START_TIME] [-e END_TIME]
                                    [-n NAMESPACE]
                                    name id

Query instance log

positional arguments:
  name                  Service name
  id                    Instance uuid

optional arguments:
  -h, --help            		show this help message and exit
  -s, --start-time=""			Logs query start time. e.g. 2015-05-01 12:12:12
  -e, --end-time=""				Logs query end time. e.g. 2015-05-01 12:12:12
  -n, --namespace=""			Service namespace
```

##compose

```
usage: alauda compose [-h] {up,ps,start,stop,restart,rm,scale} ...

Compose multi-container app

optional arguments:
  -h, --help            show this help message and exit

Alauda compose commands:
  {up,ps,start,stop,restart,rm,scale}
    up                  Create and start all service containers
    ps                  List containers
    start               Start all service containers
    stop                Stop all service containers
    restart             Restart all service containers
    rm                  Remove all service containers
    scale               Set number of containers to run for a service
```

用于一键部署应用。支持docker-compose的基本命令，并增加了alauda自身的特性。

样例：

```
bash-3.2# alauda compose up -f gitlab.alauda.yml
[alauda] Creating and starting service "postgresql"
[alauda] Creating and starting service "redis"
[alauda] Creating and starting service "gitlab"
[alauda] OK

```

##backup

```
usage: alauda backup [-h] {create,list,inspect,rm} ...

Backup operations

optional arguments:
  -h, --help            show this help message and exit

Alauda backup commands:
  {create,list,inspect,rm}
    create              Create a new volume backup
    list                List volume backups
    inspect             Get details of a volume backup
    rm                  Remove a volume backup
```

用于对服务的数据进行备份。这些数据必须是存储在卷中。

样例:

```
bash-3.2# alauda backup create backup1 redis /data
[alauda] Creating backup "backup1"
[alauda] OK

```

##organization

```
usage: alauda organization [-h] {list,create,inspect,update} ...

Organization operations

optional arguments:
  -h, --help            show this help message and exit

Alauda organization commands:
  {list,create,inspect,update}
    list                List all organization
    create              Create a new organization
    inspect             Get details of an organization
    update              Update an exist orgnization
    
```

在当前账户下创建机构，并进行管理。这些机构和普通账户一样，可以进行服务的构建等操作。管理员可以增减机构中的用户数量，或者对机构中的某一用户的权限进行修改。有只读、可写、管理员权限等。

样例:

```
bash-3.2# alauda organization list
     Name           Company              Created time
-----------------------------------------------------------
mathildedev      云雀科技研发组    2015-04-25T05:42:00.828Z
xdzhangcnorg     mathilde          2015-05-19T03:35:29.047Z
xdzhangcnorg1    mathilde2         2015-05-25T07:38:07.670Z

```
