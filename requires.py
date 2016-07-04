#!/usr/bin/python
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

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class BindRNDCRequires(RelationBase):
    scope = scopes.UNIT

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
#    auto_accessors = ['algorithm', 'rndckey', 'private-address']

    @hook('{requires:bind-rndc}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

    @hook('{requires:bind-rndc}-relation-changed')
    def changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')
        if self.data_complete():
            conv.set_state('{relation_name}.available')

    @hook('{requires:bind-rndc}-relation-{broken,departed}')
    def departed_or_broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        if not self.data_complete():
            conv.remove_state('{relation_name}.available')

    def data_complete(self):
        """
        Get the connection string, if available, or None.
        """
        if self.rndc_info() and all(self.rndc_info().values()):
            return True
        return False

    def rndc_info(self):
        """
        Get the connection string, if available, or None.
        """
        data = {}
        for conv in self.conversations():
            data = {
                'algorithm': conv.get_remote('algorithm'),
                'secret': conv.get_remote('rndckey'),
                'private_address': conv.get_remote('private-address'),
            }
            if all(data.values()):
                print(data)
                return data
        return data

    def slave_ips(self):
        values = []
        for conv in self.conversations():
            values.append({
                # Unit scoped relation so only one unit per conversation.
                'unit': list(conv.units)[0],
                'address': conv.get_remote('private-address')})
        return values

