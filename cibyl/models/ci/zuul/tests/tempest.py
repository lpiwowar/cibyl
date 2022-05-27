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
from enum import IntEnum

from overrides import overrides

from cibyl.models.ci.zuul.test import Test, TestKind, TestStatus


class TempestTestStatus(IntEnum):
    """Possible results of a Tempest test case.
    """
    UNKNOWN = 0
    """Could not determine how the test finished."""
    SUCCESS = 1
    """The test passed."""
    FAILURE = 2
    """Some condition from the test was not met."""
    SKIPPED = 3
    """The test was ignored."""
    ERROR = 4
    """The test found some error it could not recover from."""


class TempestTest(Test):
    """Model for the execution of a Tempest test case by a Zuul host.

    @DynamicAttrs: Contains attributes added on runtime.
    """

    class Data(Test.Data):
        """Holds the data that will define the model.
        """
        class_name = 'UNKNOWN'
        """Full name of the class that contains the test case."""
        skip_reason = None
        """Message indicating why the test case was ignored."""

    API = {
        **Test.API,
        'class_name': {
            'attr_type': str,
            'arguments': []
        },
        'skip_reason': {
            'attr_type': str,
            'arguments': []
        }
    }
    """Defines the base contents of the model."""

    def __init__(self, data=Data()):
        """Constructor.

        :param data: Defining data for this test.
        :type data: :class:`TempestTest.Data`
        """
        super().__init__(
            TestKind.TEMPEST,
            data,
            **{
                'class_name': data.class_name,
                'skip_reason': data.skip_reason
            }
        )

    @overrides
    def __eq__(self, other):
        if not super().__eq__(other):
            return False

        # Check this model's additional fields
        return \
            self.class_name == other.class_name and \
            self.skip_reason == other.skip_reason

    @property
    @overrides
    def status(self):
        result = self.result.value

        success_terms = [
            val.name
            for val in [TempestTestStatus.SUCCESS]
        ]

        if result in success_terms:
            return TestStatus.SUCCESS

        failed_terms = [
            val.name
            for val in [TempestTestStatus.FAILURE, TempestTestStatus.ERROR]
        ]

        if result in failed_terms:
            return TestStatus.FAILURE

        skipped_terms = [
            val.name
            for val in [TempestTestStatus.SKIPPED]
        ]

        if result in skipped_terms:
            return TestStatus.SKIPPED

        return TestStatus.UNKNOWN