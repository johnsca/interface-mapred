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


class YARNRequires(RelationBase):
    scope = scopes.GLOBAL
    auto_accessors = ['ip_addr', 'port', 'hs_http', 'hs_ipc']

    def set_local_spec(self, spec):
        """
        Set the local spec.

        Should be called after ``{relation_name}.related``.
        """
        conv = self.conversation()
        conv.set_local('spec', json.dumps(spec))

    def local_spec(self):
        conv = self.conversation()
        return json.loads(conv.get_local('spec', 'null'))

    def remote_spec(self):
        conv = self.conversation()
        return json.loads(conv.get_remote('spec', 'null'))

    def yarn_ready(self):
        conv = self.conversation()
        return conv.get_remote('yarn-ready', 'false').lower() == 'true'

    @hook('{requires:yarn}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.related')

    @hook('{requires:yarn}-relation-changed')
    def changed(self):
        conv = self.conversation()
        available = all([
            self.remote_spec() is not None,
            self.ip_addr(),
            self.port(),
            self.hs_http(),
            self.hs_ipc()])
        spec_matches = self._spec_match()
        ready = self.yarn_ready()

        conv.toggle_state('{relation_name}.spec.mismatch', available and not spec_matches)
        conv.toggle_state('{relation_name}.ready', available and spec_matches and ready)

    @hook('{requires:yarn}-relation-{departed,broken}')
    def departed(self):
        self.remove_state('{relation_name}.related')
        self.remove_state('{relation_name}.spec.mismatch')
        self.remove_state('{relation_name}.ready')

    def _spec_match(self):
        local_spec = self.local_spec()
        remote_spec = self.remote_spec()
        if None in (local_spec, remote_spec):
            return False
        for key, value in local_spec.items():
            if value != remote_spec.get(key):
                return False
        return True
