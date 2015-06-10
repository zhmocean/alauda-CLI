# Alauda Command Line

##安装

```
pip install alauda
```

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

	例如: `-t 1`

* `-a=false` 表示不显示输出此参数的情况下，参数的值为false即无效状态，如果显示的列出该参数 `-a`，则表明该参数的值为true，即有效状态。

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
  -h, --help            				show this help message and exit
  -t, --target-num-instances=1			Target number of instances for the service
  -s, --instance-size={XS,S,M,L,XL}		Service container size
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

## Login

Login命令是用于登录灵雀云美国区或者中国区系统。`-c`选项可以简单的指明所登陆的系统。`cn`为中国区，`io`为美国区。当然，你也可以使用`-e`参数来显示的指明需要登陆的地址，例如:`https://api.alauda.io/v1/`

```
usage: alauda login [-h] [-u USERNAME] [-p PASSWORD] [-c {cn,io}]
                    [-e ENDPOINT]

Alauda login

optional arguments:
  -h, --help            		show this help message and exit
  -u, --username=""				Alauda username
  -p, --password=""				Alauda password
  -c {cn,io}, --cloud={cn,io}	Alauda Cloud to connect to
  -e, --endpoint=""				Alauda API endpoint to use
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
  -t, --target-num-instances=1			Target number of instances for the service
  -s, --instance-size={XS,S,M,L,XL}		Service container size
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

* 如果显示的指明了`-a` 参数，则表明将服务设置为自动调节模式，此模式下需要使用`-f` 来指明自动调节参数配置文件所在路径。

###run

用于创建并运行一个服务。并通过参数指明服务的名称，所用镜像名称，以及服务所需容器大小，容器数量等信息。

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
  -t, --target-num-instances=1			Target number of instances for the service
  -s, --instance-size={XS,S,M,L,XL}		Service container size
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

启动处于暂停状态的服务。

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

暂停处于运行状态的服务。

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

删除已存在的服务。

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

列出当前账户下所有的服务。

###scale

调节当前服务中实例数量。

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

将当前服务的状态设置为自动调节模式。

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

必须显示指明自动调节配置文件所在位置，如果不指明，则默认当前路径下的`auto-scaling.cfg`文件为配置文件。

###disable-autoscaling

将当前服务的状态设置为手动调节模式。

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

设置为手动模式的同时，可以使用`-t`指定服务的实例数量，如果不指定，则以自动调节模式的最后实例数量为当前服务的实例数量。

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

如果不指定起始和终止时间，那么返回最近一小时以内的日志。如果只指定起始时间，那么返回指定的起始时间到当前时间的日志，如果只指定终止时间，那么返回终止时间之前一小时以内的日志。

###instances

列出服务所有的实例。

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

查看某一个实例的详细信息。

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

查看某一实例的日志信息。

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

注意：

* volumes的格式修改为path:size `path`即挂载路径，`size`为挂载卷大小单位为G。如果不指定size，则默认挂载卷大小为10G。例如:
	
	```
	volumes:
    - /data:10
    - /mnt
	```
* ports格式不再支持`port1:port2`，而如下所示:

	```
	ports:
	- "80"
	- "22"
	```
* environment。 支持环境变量的替换。即，某一环境变量可以由当前服务的其他环境变量赋值或者拼接得到。例如:

	```
	DB_HOST: $POSTGRESQL_PORT_5432_TCP_ADDR
	DB_HOST的值就是当前服务中的环境变量POSTGRESQL_PORT_5432_TCP_ADDR所指的值。
	
	``` 

* 新增size。用于指定服务所需的硬件资源大小。可选范围为{'XS', 'S', 'M', 'L', 'XL'} 例如:

	```
	size: L
	```
	
* 新增domain。 用于用户指定自己的域名。例如:

	```
	domain: "www.myself.com"
	```
	
* 新增autoscaling_config。用于指定服务的自动调节模式，以及自动调节模式的配置文件。例如:

	```
	autoscaling_config: ./autoscaling.cfg
	```
	
* 新增number。用户指定某个服务所开启的实例数量。例如:

	```
	size: 5
	```

###up

启动包含多个服务的应用。

```
usage: alauda compose up [-h] [-f FILE] [-s]

Create and start all service containers

optional arguments:
  -h, --help			show this help message and exit
  -f, --file=""			Compose file name
  -s, --strict=false	Wait for linked services to start

```
当显示的输入-s 参数时，表示服务需要等到其所link的服务启动之后，才开始启动。

###ps

列出应用的各个服务信息。

```
usage: alauda service ps [-h] [-n NAMESPACE]

List services

optional arguments:
  -h, --help            	show this help message and exit
  -n, --namespace=""		Service namespace
bash-3.2# alauda compose ps -h
usage: alauda compose ps [-h] [-f FILE]

Lists container

optional arguments:
  -h, --help			show this help message and exit
  -f, --file=""  		Compose file name
```

###start

启动已经停止的应用。

```
usage: alauda compose start [-h] [-f FILE] [-s]

Start all service containers

optional arguments:
  -h, --help           	show this help message and exit
  -f, --file=""  		Compose file name
  -s, --strict         	Wait for linked services to start
```

`-s` 同 `up`命令

###stop

暂停运行中的应用。

```
usage: alauda compose stop [-h] [-f FILE]

Stop all service containers

optional arguments:
  -h, --help           	show this help message and exit
  -f, --file=""  		Compose file name
```

###restart

重新启动应用。

```
usage: alauda compose restart [-h] [-f FILE] [-s]

Restart all service containers

optional arguments:
  -h, --help           	show this help message and exit
  -f, --file=""  		Compose file name
  -s, --strict         	Wait for linked services to start
```

###rm

删除应用。

```
usage: alauda compose rm [-h] [-f FILE]

Remove all service containers

optional arguments:
  -h, --help           	show this help message and exit
  -f, --file=""  		Compose file name
```

###scale

调节应用中每个服务的实例数量。

```
usage: alauda compose scale [-h] [-f FILE] [descriptor [descriptor ...]]

Set number of containers to run for a service

positional arguments:
  descriptor            E.g. web=2 db=1

optional arguments:
  -h, --help           	show this help message and exit
  -f, --file=""  		Compose file name
```
样例:

```
alauda compose scale web=2 redis=3
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

###create

创建备份。

```
usage: alauda backup create [-h] [-n NAMESPACE] name service dir

Create a new volume backup

positional arguments:
  name                  Backup name
  service               Name of the service to create volume backup for
  dir                   Mounted volume directory to backup

optional arguments:
  -h, --help           	show this help message and exit
  -n, --namespace=""	Service namespace
```

参数`dir` 是服务在创建的时候所制定的volume挂载路径。

###list

列出当前所有备份。

```
usage: alauda backup list [-h] [-n NAMESPACE]

list volume backups

optional arguments:
  -h, --help           	show this help message and exit
  -n, --namespace=""	Service namespace
```

###inspect

获取某个备份的详细信息。

```
usage: alauda backup inspect [-h] [-n NAMESPACE] id

Get details of a volume backup

positional arguments:
  id                    UUID of the volume backup

optional arguments:
  -h, --help           	show this help message and exit
  -n, --namespace=""	Service namespace
```

`id` 为用户创建每个备份之后所获取的唯一id。

###rm

删除备份。

```
usage: alauda backup rm [-h] [-n NAMESPACE] id

Remove a volume backup

positional arguments:
  id                    UUID of the volume backup

optional arguments:
  -h, --help           	show this help message and exit
  -n, --namespace=""	Service namespace
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
mathildedev      云雀科技研发组		2015-04-25T05:42:00.828Z
xdzhangcnorg     mathilde          2015-05-19T03:35:29.047Z
xdzhangcnorg1    mathilde2         2015-05-25T07:38:07.670Z

```
###create

创建组织。

```
usage: alauda organization create [-h] name company

Create a new organization

positional arguments:
  name        Organization name
  company     Company name

optional arguments:
  -h, --help  show this help message and exit
```

###list

列出当前用户所属的所有组织。

###inspect

获取某个组织的详细信息。

```
usage: alauda organization inspect [-h] name

Get details of an organization

positional arguments:
  name        Organization name

optional arguments:
  -h, --help  show this help message and exit
```
###update

更新某个组织的信息

```
usage: alauda organization update [-h] name company

Update an exist orgnization

positional arguments:
  name        Organization name
  company     Company name

optional arguments:
  -h, --help  show this help message and exit
```

##command completion

支持命令补全和查找。例如在输入`alauda`之后，双击`Tab`键，即可看到`alauda`支持的命令。在键入`alauda compse`之后双击`Tab`键，就可以知道`alauda compose` 所支持的命令。 当输出`alauda c`之后，单机`Tab`键，即可得到补全后的命令`alauda compose`

###Debian

只需要将源码包中的`alauda`文件拷贝到/etc/bash_completion.d，然后执行 
```
. /etc/bash_completion.d/alauda
```

###OS X

首先需要安装 bash-completion

```
$ brew install bash-completion
$ brew tap homebrew/completions
```
然后将源码包中的`alauda`文件拷贝到`/usr/local/etc/bash_completion.d/`,然后执行
```
. /usr/local/etc/bash_completion.d/alauda
```

即可。

###常见错误

##InsecurePlatformWarning

在Centos/Redhat系统，同时python 2.7.9以及以下的版本，在执行任何命令的时候，如果出现警告：

```
InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
```
可以尝试:

```
pip install pyopenssl ndg-httpsclient pyasn1
```
来解决这个问题。如果仍然无法解决这个问题，请登陆我们的系统：`https://www.alauda.cn` 提交工单，联系我们。
或者在github上提交issue。