"""
#    Copyright 2022 Red Hat
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
"""
import yaml
from yaml import YAMLError as YAMLLoadError


class YAMLError(Exception):
    """Represents an error occurring while a YAML file is being parsed.
    """


def parse(file: str) -> dict:
    """Reads a YAML file.

    :param file: Path to the YAML file to be read.
    :return: The contents of the YAML file.
    :raises YAMLError: If the file failed to be loaded.
    """
    try:
        with open(file, 'r', encoding='utf8') as buffer:
            return yaml.safe_load(buffer)
    except (OSError, YAMLLoadError) as ex:
        raise YAMLError(f"Failed to parse file: '{file}'") from ex


def encrypted_constructor(loader: yaml.SafeLoader,
                          node: yaml.nodes.MappingNode):
    """
    Construct an ecrypted token.
    """
    return ""


def get_loader():
    """
    Add constructors to PyYAML loader.
    """
    loader = yaml.SafeLoader
    loader.add_constructor("!encrypted/pkcs1-oaep", encrypted_constructor)
    return loader
