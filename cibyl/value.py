# Copyright 2022 Red Hat
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


class ValueInterface(object):

    def __init__(self, name, arg_name=None, type=None):
        self.name = name
        self.arg_name = arg_name
        self.type = type


class Value(ValueInterface):

    def __init__(self, name, arg_name=None, type=None, data=None):
        super(Value, self).__init__(name, arg_name, type)
        self.data = data


class ListValue(ValueInterface):

    def __init__(self, name, arg_name=None, type=None, data=[]):
        super(ListValue, self).__init__(name, arg_name, type)
        if isinstance(data, list):
            self.data = data

    def append(self, item):
        self.data.append(item)
