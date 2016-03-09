# Overview

This interface layer handles the communication with YARN via the `mapred` interface
protocol.  It is intended for internal use within the Hadoop cluster charms.
!!!! For typical usage, [interface-hadoop-plugin][] should be used instead. !!!!


# Usage

## Requires

Charms requiring this interface can be clients, or NodeManagers.
Clients simply depend on YARN to provide as a distributed compute to them, while
NodeManagers register to provide additional services back.

This interface layer will set the following states, as appropriate:

  * `{relation_name}.joined` The relation is established, but YARN may not yet
    have provided any connection or service information.

  * `{relation_name}.ready` YARN has provided its connection and service
    information, and is ready to provide compute services.
    The provided information can be accessed via the following methods:
      * `hosts_map()`
      * `port()`
      * `hs_http()`
      * `hs_ipc()`

For example, a typical client would respond to `{relation_name}.ready`:

```python
@when('flume.installed', 'yarn.ready')
def yarn_ready(yarn):
    flume.configure(yarn)
    flume.start()
```


## Provides

A charm providing this interface is providing the YARN service.

This interface layer will set the following states, as appropriate:

  * `{relation_name}.clients` One or more clients of any type have
    been related.  The charm should call the following methods to provide the
    appropriate information to the clients:
      * `send_spec(spec)`
      * `send_hosts_map(hosts)`
      * `send_ports(port, historyserver_web_port, historyserver_ipc_port)`
      * `send_ready(ready)`

Example:

```python
@when('resourcemanager.clients')
@when('yarn.ready')
def serve_client(client):
    client.send_spec(utils.build_spec())
    client.send_ports(dist_config.get('port'), dist_config.get('webyarn_port'))
    client.send_ready(True)

@when('resourcemanager.clients')
@when_not('yarn.ready')
def check_ready(client):
    client.send_ready(False)
```


# Contact Information

- <bigdata@lists.ubuntu.com>


# Hadoop

- [Apache Hadoop](http://hadoop.apache.org/) home page
- [Apache Hadoop bug trackers](http://hadoop.apache.org/issue_tracking.html)
- [Apache Hadoop mailing lists](http://hadoop.apache.org/mailing_lists.html)
- [Apache Hadoop Juju Charm](http://jujucharms.com/?text=hadoop)
