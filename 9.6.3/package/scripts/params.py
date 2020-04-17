#coding=utf8
"""

"""
from resource_management import *
import json
import socket
import os.path

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

postgresql_user = config['configurations']['postgresql-env']['postgresql_user']
postgresql_group = config['configurations']['postgresql-env']['postgresql_group']
postgresql_base_dir = config['configurations']['postgresql-env']['postgresql_base_dir']
postgresql_source_dir = config['configurations']['postgresql-env']['postgresql_source_dir']
# postgresql_conf_dir = config['configurations']['postgresql-env']['postgresql_conf_dir']
postgresql_log_dir = config['configurations']['postgresql-env']['postgresql_log_dir']
# postgresql_pid_dir = config['configurations']['postgresql-env']['postgresql_pid_dir']
# postgresql_pid_file = format("{postgresql_base_dir}/data/postmaster.pid")
postgresql_pid_file = config['configurations']['postgresql-env']['postgresql_pid_file']

postgresql_install_log = postgresql_base_dir + '/postgresql-install.log'
# path_data = config['configurations']['postgresql-config']['path_data']
path_logs = config['configurations']['postgresql-config']['path_logs']
postgresql_download = config['configurations']['postgresql-config']['download_website']

# bootstrap_memory_lock = str(config['configurations']['postgresql-config']['bootstrap_memory_lock'])

# # Postgresql expetcs that boolean values to be true or false and will generate an error if you use True or False.
# if bootstrap_memory_lock == 'True':
#     bootstrap_memory_lock = 'true'
# else:
#     bootstrap_memory_lock = 'false'
#
# network_host = config['configurations']['postgresql-config']['{network_host']
# http_port = config['configurations']['postgresql-config']['http_port']


