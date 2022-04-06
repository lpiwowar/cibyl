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
from unittest import TestCase
from unittest.mock import Mock

import cibyl
from cibyl.cli.main import raw_parsing
from cibyl.cli.output import OutputStyle
from cibyl.exceptions.cli import InvalidArgument


class TestRawParsing(TestCase):
    def test_default_output(self):
        args = raw_parsing([])

        self.assertTrue(OutputStyle.COLORED, args['output_style'])

    def test_o_arg(self):
        output = 'raw'

        parse_call = cibyl.cli.main.OutputStyle.from_str = Mock()
        parse_call.return_value = OutputStyle.RAW

        args = raw_parsing(['', '-o', output])

        self.assertTrue(OutputStyle.RAW, args['output_style'])

        parse_call.assert_called_once_with(output)

    def test_output_arg(self):
        output = 'raw'

        parse_call = cibyl.cli.main.OutputStyle.from_str = Mock()
        parse_call.return_value = OutputStyle.RAW

        args = raw_parsing(['', '--output', output])

        self.assertTrue(OutputStyle.RAW, args['output_style'])

        parse_call.assert_called_once_with(output)

    def test_invalid_output_arg(self):
        def raise_error(_):
            raise NotImplementedError

        output = 'invalid'

        parse_call = cibyl.cli.main.OutputStyle.from_str = Mock()
        parse_call.side_effect = raise_error

        with self.assertRaises(InvalidArgument):
            raw_parsing(['', '--output', output])

        parse_call.assert_called_once_with(output)
