#!/opt/mm-agent/python/bin/python
#
# Testing this plugin on cmd-line:
# MYSQL_USER=root MYSQL_PASS=secret-password MYSQL_HOST=localhost /opt/mm-agent/python/bin/python mysql.py
#
# Remember to edit mysql.py.conf with the correct configuration
#
import MySQLdb
import os

SHOW_ALL_METRICS=False

connect_overrides = {
    'MYSQL_USER': 'user',
    'MYSQL_HOST': 'host',
    'MYSQL_PASS': 'passwd',
}
connect_options = { }

COUNTER_ENDINGS = [
    'read',
    'written',
    'sent',
    'received',
    'queries',
    'questions',
    '_rows_read',
    '_rows_updated',
    '_rows_deleted',
    '_rows_inserted',
]

COUNTER_NAMES = [
    'connections',
    'created_tmp_disk_tables',
    'created_tmp_files', 
    'created_tmp_tables',
    'qcache_hits',
]

COUNTER_PREFIXES = [
    'handler_',
    'com_',
]

IMPORTANT_METRICS = [
    'aborted_clients',
    'aborted_connects',
    'qcache_hits',
    'qcache_hits',
    'questions',
    'queries',
    'com_select',
    'com_insert',
    'com_delete',
    'com_update',
    'connections',
    'slow_queries',
]

METRIC_NAME_MAP = {
    'connections': 'total_connections',
    'aborted_clients': 'total_aborted_clients',
    'aborted_connects': 'total_aborted_connects',
}

def readConfigValue(configKeyName, default):
    """
    Find value of configKeyName. Return true
    if the value exists and is 1, yes or true,
    otherwise return false. Return default if
    not found
    """
    if not configKeyName in os.environ:
        return default
    value = os.environ[configKeyName].lower()
    if value in ['yes', 'true', '1']:
        return True
    return False

def shouldIncludeMetric(name):
    """
    If we should include or ignore metric
    """
    if SHOW_ALL_METRICS:
        return True

    if name in IMPORTANT_METRICS:
        return True
    return False

def cloneCertainKeys(name, value):
    """
    For some keys we want a total and a rate. Print the rate here,
    while the total version will be printed the "normal" way
    """
    if name in ['connections', 'aborted_clients', 'aborted_connections']:
        print "_counter.mysql.rate.%s: %s" % (keyname, value)

def getPerformanceData():
    c.execute('''
SELECT schema_name, ROUND((SUM(sum_timer_wait)/ SUM(count_star)) / 1000000) AS avg_micros
FROM performance_schema.events_statements_summary_by_digest
WHERE schema_name IS NOT NULL
GROUP BY schema_name
    ''')
    for row in c.fetchall():
        schema_name = row[0]
        avg_micros = row[1]
        print "mysql.performance.%s.avg_wait_micros: %s" % (schema_name, avg_micros)

SHOW_ALL_METRICS = readConfigValue('SHOW_ALL_METRICS', False)
SHOW_PERFORMANCE_DATA = readConfigValue('SHOW_PERFORMANCE_DATA', True)

for key, value in connect_overrides.iteritems():
    if not key in os.environ or not os.environ[key]:
        continue
    connect_options[value] = os.environ[key]

m = MySQLdb.connect(**connect_options)
c = m.cursor()
c.execute('SHOW GLOBAL STATUS')
for row in c.fetchall():
    keyname = row[0].lower().replace(' ', '_')

    if not shouldIncludeMetric(keyname):
        continue

    cloneCertainKeys(keyname, row[1])

    if keyname in METRIC_NAME_MAP:
        keyname = METRIC_NAME_MAP[keyname]

    counter = ''
    for name in COUNTER_NAMES:
        if keyname == name:
            counter = '_counter.'

    for ending in COUNTER_ENDINGS:
        if keyname.endswith(ending):
            counter = '_counter.'

    for start in COUNTER_PREFIXES:
        if keyname.startswith(start):
            counter = '_counter.'

    print "%smysql.%s: %s" % (counter, keyname, row[1])

if SHOW_PERFORMANCE_DATA:
    try:
        getPerformanceData()
    except:
        pass
