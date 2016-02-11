# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class MapredProvides(RelationBase):
    scope = scopes.UNIT

    @hook('{provides:mapred}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.clients')

    @hook('{provides:mapred}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.clients')

    def send_spec(self, spec):
        for conv in self.conversations():
            conv.set_remote('spec', json.dumps(spec))

    def send_resourcemanagers(self, resourcemanagers):
        for conv in self.conversations():
            conv.set_remote('resourcemanagers', json.dumps(resourcemanagers))

    def send_ports(self, port, hs_http, hs_ipc):
        for conv in self.conversations():
            conv.set_remote(data={
                'port': port,
                'historyserver-http': hs_http,
                'historyserver-ipc': hs_ipc,
            })

    def send_ready(self, ready=True):
        for conv in self.conversations():
            conv.set_remote('has_slave', ready)

    def send_hosts_map(self, hosts_map):
        for conv in self.conversations():
            conv.set_remote('etc_hosts', json.dumps(hosts_map))
