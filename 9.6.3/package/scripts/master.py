#!/usr/bin/env python

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os
import glob
import signal
import time
import pwd
import grp
from resource_management import *
from postgresql_common import kill_process

class Master(Script):

    # install elasticsearch
    def install(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.elastic_pid_file property as
        # format('{elastic_pid_file}')
        env.set_params(params)

        # Install dependent packages
        self.install_packages(env)

        # Create user and group for Postgresql if they don't exist

       # try: grp.getgrnam(params.postgreql_group)
       # except KeyError: Group(group_name=params.postgresql_group)

        try: pwd.getpwnam(params.postgresql_user)
        except KeyError: os.system("useradd %s" % params.postgresql_user)

        # Create Postgresql directories
        Directory([params.postgresql_base_dir, params.postgresql_source_dir, params.postgresql_log_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.postgresql_user,
                  group=params.postgresql_group,
                  create_parents=True
                 )
        # Create empty Postgresql install log
        File([params.postgresql_install_log,params.postgresql_pid_file],
             mode=0644,
             owner=params.postgresql_user,
             group=params.postgresql_group,
             content=''
            )

        # Download Postgresql
        cmd = format("cd {postgresql_source_dir}; wget {postgresql_download} -O postgresql-9.6.3.tar.gz -a {postgresql_install_log}")
        Execute(cmd, user=params.postgresql_user)

        # Install Postgresql
        cmd = format("cd {postgresql_source_dir}; tar -xf  postgresql-9.6.3.tar.gz")
        Execute(cmd, user=params.postgresql_user)

        # Ensure all files owned by postgresql user
        cmd = format("chown -R {postgresql_user}:{postgresql_group} {postgresql_base_dir}")
        Execute(cmd)

        # Install dependence
        cmd = format("yum install readline* -y && yum install zlib-devel -y && yum install libpq.so* -y")
        Execute(cmd)

        # Make install
        cmd = format("cd {postgresql_source_dir}/postgresql-9.6.3; ./configure --prefix={postgresql_base_dir} --enable-debug ; make && make install")
        Execute(cmd)

        cmd = format("chown -R postgres:postgres {postgresql_base_dir}")
        Execute(cmd)

        # Remove postgresql installation file
        cmd = format("cd {postgresql_source_dir}; rm -rf postgresql-9.6.3.tar.gz")
        Execute(cmd, user=params.postgresql_user)

        # Ensure all files owned by postgresql user
        cmd = format("chown -R {postgresql_user}:{postgresql_group} {postgresql_base_dir}")
        Execute(cmd)

        # Vim .bashrc
        cmd = format("echo 'export PGHOME=/opt/postgresql' >>/home/postgres/.bash_profile ; echo 'export PGDATA=/opt/postgresql/data' >>/home/postgres/.bash_profile ; echo 'export export PATH=$PGHOME/bin:$PATH' >>/home/postgres/.bash_profile ; source /home/postgres/.bash_profile " )
        Execute(cmd, user=params.postgresql_user)

        # Initdb
        cmd = format("{postgresql_base_dir}/bin/initdb -D /opt/postgresql/data")
        Execute(cmd, user=params.postgresql_user)


        Execute('echo "Install complete"')


    def configure(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.postgresql_pid_file property as
        # format('{postgresql_pid_file}')
        env.set_params(params)

        configurations = params.config['configurations']['postgresql-config']

        File(format("{postgresql_base_dir}/data/postgresql.conf"),
             content=Template("postgresql.conf.j2",
                              configurations=configurations),
             owner=params.postgresql_user,
             group=params.postgresql_group
            )
        File(format("{postgresql_base_dir}/data/pg_hba.conf"),
             content=Template("pg_hba.conf.j2",
                              configurations=configurations),
             owner=params.postgresql_user,
             group=params.postgresql_group
             )

        Execute('echo "Configuration complete"')

    def stop(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the params.elastic_pid_file property as
        #  format('{elastic_pid_file}')
        env.set_params(params)

        # Stop Postgresql
        cmd = format("{postgresql_base_dir}/bin/pg_ctl -D {postgresql_base_dir}/data -l {postgresql_log_dir}/psql.log stop")
        Execute(cmd, user=params.postgresql_user)
        kill_process(params.postgresql_pid_file, params.postgresql_user, params.postgresql_log_dir)


    def start(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.elastic_pid_file property as
        #  format('{elastic_pid_file}')
        env.set_params(params)

        # Configure Postgresql
        self.configure(env)

        # Start Postgresql
        cmd = format("{postgresql_base_dir}/bin/pg_ctl -D {postgresql_base_dir}/data -l {postgresql_log_dir}/psql.log start")
        Execute(cmd, user=params.postgresql_user)


    # @staticmethod
    def status(self, env):
        # Import properties defined in -env.xml file from the status_params class
        import status_params
        import params

        # This allows us to access the params.elastic_pid_file property as
        #  format('{elastic_pid_file}')
        env.set_params(status_params)

        #try:
        #    pid_file = glob.glob(status_params.postgresql_pid_file)[0]
        #except IndexError:
        #    pid_file = ''

        # Use built-in method to check status using pidfile
        # check_process_status(status_params.postgresql_pid_file)
        # File(status_params.postgresql_pid_file,
        #      mode=0644,
        #      owner=params.postgresql_user,
        #      group=params.postgresql_group,
        #      content=''
        #      )

        # cmd = format("echo '{status_params.postgresql_pid}'> {params.postgresql_pid_file}")
        # Execute(cmd, user=params.postgresql_user)
        import os
        os.system("ps -ef|grep postgresql|grep -v grep|awk '{print $2}'> /opt/postgresql/postgresql.pid")
        check_process_status(params.postgresql_pid_file)

if __name__ == "__main__":
    Master().execute()