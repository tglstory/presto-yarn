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

from resource_management import *
from configure import set_configuration


class Prestoserver(Script):
    def install(self, env):
        self.install_packages(env)
        pass

    def configure(self, env):
        # TODO: set_configuration should be called for coordinator and workers
        # (probably via a component name arg)
        set_configuration()

    def start(self, env):
        import params
        env.set_params(params)
        
        self.configure(env)
        process_cmd = format("PATH={java8_home}/bin:$PATH {presto_root}/bin/launcher start")

        Execute(process_cmd,
                logoutput=False,
                wait_for_finish=False,
                pid_file=params.server_pid_file,
                poll_after=5
        )

    def stop(self, env):
        import params

        env.set_params(params)
        # Slider doesnt yet support stopping the actual app (PrestoServer) process
        # but only stopping the yarn application
        # TODO: try using launcher.py stop 

    def status(self, env):
        import params

        env.set_params(params)
        check_process_status(params.server_pid_file)


if __name__ == "__main__":
    Prestoserver().execute()
