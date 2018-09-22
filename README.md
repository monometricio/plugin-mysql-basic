# plugin-mysql-basic
Monometric.IO mysql plugin (https://monometric.io)

## Description

This plugin will query mysql for stats. If you include performance schema, you can also get the average wait time for all databases.

## Installation

```mm-plugins install monometricio/plugin-mysql-basic```

```mm-plugins enable monometricio/plugin-mysql-basic```

You should see the plugin when running ```mm-plugins list```.

Remember to edit the configuration file ```/etc/mm-agent/plugins/monometricio-plugin-mysql-basic.conf```.

## Configuration

The plugin has the following optional configuration keys:

- MYSQL_PASS
- MYSQL_HOST
- MYSQL_PORT
- SHOW_ALL_METRICS -- this config value exposes additional data to the metric, not needed for most people

To include the performance schema in mysql, add ```performance_schema=ON``` to
my.cnf. Please remember that this can result in a ~5% overhead. For more
information, visit
https://dev.mysql.com/doc/refman/8.0/en/performance-schema.html

## Testing configuration

You can test-run the plugin and verify the output by running:

```mm-plugins run monometricio/plugin-mysql-basic```
