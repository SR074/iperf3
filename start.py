from datetime import datetime, timedelta, timezone

import configparser
import subprocess
import json
import mysql.connector

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

subprocess.run(
    [config_ini['iperf3']['dir'], "-c", config_ini['iperf3']['AccessPoint'], "-p", config_ini['iperf3']['port'],
     "--logfile", "temp.json", "-J"])

json_open = open('temp.json', 'r')
res_json = json.load(json_open)

config = {
    'user': config_ini['mysql']['User'],
    'password': config_ini['mysql']['Password'],
    'host': config_ini['mysql']['Host'],
    'port': config_ini['mysql']['Port'],
    'database': config_ini['mysql']['Database'],
}
cnx = mysql.connector.connect(**config)
cnx.ping(reconnect=True)
cursor = cnx.cursor()

host_id = config_ini['mysql']['HostId']
remote_id = config_ini['mysql']['RemoteId']

send_bytes = res_json['end']['sum_sent']['bytes']
send_bps = res_json['end']['sum_sent']['bits_per_second']
receive_bytes = res_json['end']['sum_received']['bytes']
receive_bps = res_json['end']['sum_received']['bits_per_second']
cpu_util_host = res_json['end']['cpu_utilization_percent']['host_total']
cpu_util_remote = res_json['end']['cpu_utilization_percent']['remote_total']
timestamp = res_json['start']['timestamp']['time']
created = datetime.now(timezone(timedelta(hours=+9), 'JST'))

sql = 'insert into results (host_id, remote_id, send_bytes, send_bps, receive_bytes, receive_bps, cpu_util_host, cpu_util_remote, timestamp, created) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
cursor.execute(sql, host_id, remote_id, send_bytes,send_bps,receive_bytes,receive_bps,cpu_util_host,cpu_util_remote,timestamp,created)

cursor.close()
cnx.close()
