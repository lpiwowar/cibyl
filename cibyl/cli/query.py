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
from typing import Optional

from cibyl.utils.dicts import subset


class QueryType(IntEnum):
    """Defines the hierarchy level at which a query is meant to be performed.
    """
    NONE = 0
    """No data from host is requested."""
    FEATURES = 1
    """Retrieve data using features."""
    TENANTS = 2
    """Only retrieve data concerning tenants."""
    PROJECTS = 3
    """Retrieve data concerning projects and above."""
    PIPELINES = 4
    """Retrieve data concerning pipelines and above."""
    JOBS = 5
    """Retrieve data concerning jobs and above."""
    VARIANTS = 6
    """Retrieve data concerning job variants and above."""
    BUILDS = 7
    """Retrieve data concerning builds and above."""
    TESTS = 8
    """Retrieve data concerning tests and above."""
    FEATURES_JOBS = 9
    """Retrieve data using features and jobs."""


class QuerySelector:
    """Deduce the type of query performed from the cli argument considering
    both core argument and plugin provided ones."""
    query_selector_functions = []

    def get_query_type_core(self, command: Optional[str] = None,
                            **kwargs) -> QueryType:
        """Deduces the type of query from a set of arguments related to cibyl
        core ci models.

        :param command: Which cibyl subcommand was executed, it's used
        essentially to detect whether the features subcommand was called
        :param kwargs: The arguments.
        :key tenants: Query targets tenants.
        :key projects: Query targets projects.
        :key pipelines: Query targets pipelines.
        :key jobs: Query targets jobs.
        :key variants: Query targets job variants.
        :key builds: Query target builds.
        :key tests: Query target tests.
        :return: The lowest query level possible. For example,
            if both 'tenants' and 'builds' are requested, this will choose
            'builds' over 'tenants'.
        """

        result = QueryType.NONE

        if 'tenants' in kwargs:
            result = QueryType.TENANTS

        if 'projects' in kwargs:
            result = QueryType.PROJECTS

        if 'pipelines' in kwargs:
            result = QueryType.PIPELINES

        job_args = subset(kwargs, ["jobs", "job_url"])
        if job_args:
            result = QueryType.JOBS

        if 'variants' in kwargs:
            result = QueryType.VARIANTS

        build_args = subset(kwargs, ["builds", "last_build", "build_status"])
        if build_args:
            result = QueryType.BUILDS

        test_args = subset(kwargs, ["tests", "test_result", "test_duration"])
        if test_args:
            result = QueryType.TESTS

        if command == 'features':
            if job_args:
                result = QueryType.FEATURES_JOBS
            else:
                result = QueryType.FEATURES

        return result

    def get_type_query(self, command: Optional[str] = None,
                       **kwargs) -> QueryType:
        """Deduce the type of query from the given arguments, taking into
        account arguments provided by the plugins, if present. It will return
        the largest query type provided by either the core types or the
        plugins.

        :param command: Which cibyl subcommand was executed, it's used
        essentially to detect whether the features subcommand was called
        """
        core_query = self.get_query_type_core(command=command, **kwargs)
        plugins_query = QueryType.NONE
        if self.query_selector_functions:
            plugins_query = max([get_query(**kwargs) for get_query in
                                 self.query_selector_functions])
        return max(core_query, plugins_query)


def get_query_type(command: Optional[str] = None, **kwargs) -> QueryType:
    """Deduces the type of query from a set of arguments.

    :param command: Which cibyl subcommand was executed, it's used
    essentially to detect whether the features subcommand was called
    :param kwargs: The arguments.
    :key tenants: Query targets tenants.
    :key projects: Query targets projects.
    :key pipelines: Query targets pipelines.
    :key jobs: Query targets jobs.
    :key builds: Query target builds.
    :return: The lowest query level possible. For example,
        if both 'tenants' and 'builds' are requested, this will choose
        'builds' over 'tenants'.
    """
    query_selector = QuerySelector()
    return query_selector.get_type_query(command=command, **kwargs)
