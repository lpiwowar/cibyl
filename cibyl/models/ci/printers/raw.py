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
from cibyl.cli.query import QueryType
from cibyl.models.ci.printers.colored import CIColoredPrinter
from cibyl.utils.colors import ClearText


class CIRawPrinter(CIColoredPrinter):
    """Same as :class:`CIColoredPrinter`, but this one removes all color
    decoration, leaving only the raw text.
    """

    def __init__(self, query=QueryType.NONE, verbosity=0):
        """Constructor.

        See parents for more information.
        """
        super().__init__(query, verbosity, ClearText())