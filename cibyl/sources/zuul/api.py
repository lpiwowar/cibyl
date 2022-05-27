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
from abc import ABC, abstractmethod

from cibyl.exceptions.source import SourceException
from cibyl.sources.zuul.apis.builds import Artifact, ArtifactKind
from cibyl.sources.zuul.providers import JobsProvider, PipelinesProvider
from cibyl.utils.io import Closeable


class ZuulAPIError(SourceException):
    """Represents an error occurring while performing a call to Zuul's API
    """


class ZuulBuildAPI(Closeable, ABC):
    """Interface which defines the information that can be retrieved from
    Zuul regarding a particular build.
    """

    def __init__(self, job, build):
        """Constructor.

        :param job: Job this build belongs to.
        :type job: :class:`ZuulJobAPI`
        :param build: Description of the build being consulted by this API.
        Minimum fields are: 'project', 'pipeline', 'uuid', 'result' and
        'duration'.
        :type build: dict
        """
        self._job = job
        self._build = build

    @property
    def job(self):
        """
        :return: The job this build belongs to.
        :rtype: :class:`ZuulJobAPI`
        """
        return self._job

    @property
    def project(self):
        """
        :return: Name of the project this build belongs to.
        :rtype: str
        """
        return self._build['project']

    @property
    def pipeline(self):
        """
        :return: Name of the pipeline that triggered this build.
        :rtype: str
        """
        return self._build['pipeline']

    @property
    def uuid(self):
        """
        :return: The build's identifier.
        :rtype: str
        """
        return self._build['uuid']

    @property
    def result(self):
        """
        :return: The build's result.
        :rtype: str
        """
        return self._build['result']

    @property
    def duration(self):
        """
        :return: How long the build took to complete, in ms.
        :rtype: int
        """
        return self._build['duration']

    @property
    def artifacts(self):
        result = []

        for entry in self._build['artifacts']:
            artifact = Artifact()

            if 'name' in entry:
                artifact.name = entry['name']

            if 'url' in entry:
                artifact.url = entry['url']

            if 'metadata' in entry:
                metadata = entry['metadata']

                if 'type' in metadata:
                    artifact.type = ArtifactKind.from_string(metadata['type'])

            result.append(artifact)

        return result

    @property
    def raw(self):
        """
        :return: All the data known of this build, unprocessed.
        :rtype: dict
        """
        return self._build

    @abstractmethod
    def tests(self):
        """
        :return: The tests run by this build.
        :rtype: list[:class:`ZuulTestAPI`]
        """
        raise NotImplementedError


class ZuulJobAPI(Closeable, ABC):
    """Interface which defines the information that can be retrieved from
    Zuul regarding a particular job.
    """

    def __init__(self, tenant, job):
        """Constructor.

        :param tenant: Tenant this job belongs to.
        :type tenant: :class:`ZuulTenantAPI`
        :param job: Description of the job being consulted by this
            API. At least a field called 'name' providing the name
            of the job is required here.
        :type job: dict
        """
        self._tenant = tenant
        self._job = job

    @property
    def tenant(self):
        """
        :return: The tenant this job belongs to.
        :rtype: :class:`ZuulTenantAPI`
        """
        return self._tenant

    @property
    def name(self):
        """
        :return: Name of the job being consulted.
        :rtype: str
        """
        return self._job['name']

    @property
    @abstractmethod
    def url(self):
        """
        :return: URL where this job can be consulted at.
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def variants(self):
        """
        :return: The variants of this job.
        :rtype: list[dict]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError

    @abstractmethod
    def builds(self):
        """
        :return: The builds of this job.
        :rtype: list[:class:`ZuulBuildAPI`]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError


class ZuulPipelineAPI(Closeable, JobsProvider, ABC):
    """Interface which defines the information that can be retrieved from
    Zuul regarding a particular pipeline.
    """

    def __init__(self, project, pipeline):
        """Constructor.

        :param project: Project this pipeline belongs to.
        :type project: :class:`ZuulProjectAPI`
        :param pipeline: Description of the pipeline being consulted by this
            API. At least a field called 'name' providing the name
            of the pipeline is required here.
        :type pipeline: dict
        """
        self._project = project
        self._pipeline = pipeline

    @property
    def project(self):
        """
        :return: The project this pipeline belongs to.
        :rtype: :class:`ZuulProjectAPI`
        """
        return self._project

    @property
    def name(self):
        """
        :return: Name of this pipeline.
        :rtype: str
        """
        return self._pipeline['name']

    @abstractmethod
    def jobs(self):
        """
        :return: The jobs on this pipeline.
        :rtype: list[:class:`ZuulJobAPI`]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError


class ZuulProjectAPI(Closeable, PipelinesProvider, ABC):
    """Interface which defines the information that can be retrieved from
    Zuul regarding a particular project.
    """

    def __init__(self, tenant, project):
        """Constructor.

        :param tenant: Tenant this job belongs to.
        :type tenant: :class:`ZuulTenantAPI`
        :param project.: Description of the project being consulted by this
            API. At least a field called 'name' providing the name
            of the project is required here.
        :type project: dict
        """
        self._tenant = tenant
        self._project = project

    @property
    def tenant(self):
        """
        :return: The tenant this project belongs to.
        :rtype: :class:`ZuulTenantAPI`
        """
        return self._tenant

    @property
    def name(self):
        """
        :return: Name of the project being consulted.
        :rtype: str
        """
        return self._project['name']

    @property
    @abstractmethod
    def url(self):
        """
        :return: URL where this project can be consulted at.
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def pipelines(self):
        """
        :return: The pipelines on this project.
        :rtype: list[:class:`ZuulPipelineAPI`]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError


class ZuulTenantAPI(Closeable, JobsProvider, ABC):
    """Interface which defines the information that can be retrieved from
    Zuul regarding a particular tenant.
    """

    def __init__(self, tenant):
        """Constructor.

        :param tenant: Description of the tenant being consulted by this
            API. At least a field called 'name' providing the name
            of the tenant is required here.
        :type tenant: dict
        """
        self._tenant = tenant

    @property
    def name(self):
        """
        :return: Name of the tenant being consulted.
        :rtype: str
        """
        return self._tenant['name']

    @abstractmethod
    def builds(self):
        """A build is an instance of a job running independently.

        :return: Information about all executed builds under this tenant.
        :rtype: list[dict]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError

    @abstractmethod
    def buildsets(self):
        """A buildset is a collection of builds running under a common context.

        :return: Information about all executed buildsets under this tenant.
        :rtype: list[dict]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError

    @abstractmethod
    def projects(self):
        """A project is the representation of a source code that Zuul is
        meant to interact with.

        :return: Information about all projects under this tenant.
        :rtype: list[:class:`ZuulProjectAPI`]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError

    @abstractmethod
    def jobs(self):
        """A job describes the steps that need to be taken in order to test
        a project.

        :return: Information about all jobs under this tenant.
        :rtype: list[:class:`ZuulJobAPI`]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError


class ZuulAPI(Closeable, ABC):
    """Interface describing the actions that can be taken over Zuul's API.
    """

    @abstractmethod
    def info(self):
        """Information which define the target host. Among this info there
        are entries such as 'capabilities' or 'authentication' param.

        :return: General information about the host.
        :rtype: dict
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError

    @abstractmethod
    def tenants(self):
        """Gets all tenants currently present on the host.

        :return: A sub-api to retrieve information about all tenants on the
            host.
        :rtype: list[:class:`ZuulTenantAPI`]
        :raises ZuulAPIError: If the request failed.
        """
        raise NotImplementedError
