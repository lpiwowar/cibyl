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

from cibyl.models.ci.zuul.test import Test, TestKind, TestStatus


class TestTest(TestCase):
    """Tests for :class:`Test`.
    """

    def test_attributes(self):
        """Checks that the model has the desired attributes.
        """
        kind = TestKind.ANSIBLE
        name = 'test'
        status = TestStatus.SUCCESS
        duration = 1.2
        url = 'url-to-test'

        data = Test.Data()
        data.name = name
        data.status = status
        data.duration = duration
        data.url = url

        model = Test(kind, data)

        self.assertEqual(kind, model.kind.value)
        self.assertEqual(name, model.name.value)
        self.assertEqual(status, model.status.value)
        self.assertEqual(duration, model.duration.value)
        self.assertEqual(url, model.url.value)

    def test_equality_by_type(self):
        """Checks that two models are no the same if they are of different
        type.
        """
        model = Test(TestKind.UNKNOWN, Test.Data())
        other = Mock()

        self.assertNotEqual(other, model)

    def test_equality_by_reference(self):
        """Checks that a model is equal to itself.
        """
        model = Test(TestKind.UNKNOWN, Test.Data())

        self.assertEqual(model, model)

    def test_equality_by_contents(self):
        """Checks that two models are equal if they hold the same data.
        """
        data = Test.Data()
        data.name = 'test'
        data.status = TestStatus.SUCCESS
        data.duration = 1.2
        data.url = 'url-to-test'

        model1 = Test(TestKind.ANSIBLE, data)
        model2 = Test(TestKind.ANSIBLE, data)

        self.assertEqual(model2, model1)
