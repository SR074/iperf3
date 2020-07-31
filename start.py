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
json_load = json.load(json_open)

config = {
    'user': config_ini['mysql']['User'],
    'password': config_ini['mysql']['Password'],
    'host': config_ini['mysql']['Host'],
    'port':config_ini['mysql']['Port'],
    'database': config_ini['mysql']['Database'],
}
cnx = mysql.connector.connect(**config)
cnx.ping(reconnect=True)
cursor = cnx.cursor()

get_results_last_id = select *
push_id = get_results_last_id + 1
cursor.


