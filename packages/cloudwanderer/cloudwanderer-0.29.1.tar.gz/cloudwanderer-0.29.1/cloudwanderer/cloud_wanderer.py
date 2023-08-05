"""Main cloudwanderer module."""
import concurrent.futures
import logging
from datetime import datetime
from typing import Callable, Dict, List, NamedTuple, Optional, Union

from .aws_interface import CloudWandererAWSInterface
from .base import CloudInterface, ServiceResourceTypeFilter
from .cloud_wanderer_resource import CloudWandererResource
from .models import ServiceResourceType
from .storage_connectors import BaseStorageConnector
from .urn import URN, PartialUrn
from .utils import exception_logging_wrapper

logger = logging.getLogger("cloudwanderer")


class CloudWanderer:
    """CloudWanderer."""

    def __init__(
        self, storage_connectors: List["BaseStorageConnector"], cloud_interface: CloudInterface = None
    ) -> None:
        """Initialise CloudWanderer.

        Args:
            storage_connectors:
                CloudWanderer storage connector objects.
            cloud_interface:
                The cloud interface to get resources from.
                Defaults to :class:`~cloudwanderer.aws_interface.CloudWandererAWSInterface`.
        """
        self.storage_connectors = storage_connectors
        self.cloud_interface = cloud_interface or CloudWandererAWSInterface()

    def write_resource(
        self, urn: URN, service_resource_type_filters: Optional[List[ServiceResourceTypeFilter]] = None
    ) -> None:
        """Fetch data for and persist to storage a single resource and its subresources.

        If the resource does not exist it will be deleted from the storage connectors.

        Example:
            Fetch a specific VPC and write it to a local Gremlin database.

                >>> from cloudwanderer import CloudWanderer, ServiceResourceType, URN
                >>> from cloudwanderer.storage_connectors import GremlinStorageConnector
                >>> cloud_wanderer = CloudWanderer(storage_connectors=[
                ...        GremlinStorageConnector(
                ...          endpoint_url="ws://localhost:8182",
                ...        )
                ...    ])
                >>> cloud_wanderer.write_resource(
                ...     urn=URN.from_string("urn:aws:123456789012:us-east-1:ec2:vpc:vpc-11111111")
                ... )

        Arguments:
            urn (URN):
                The URN of the resource to write
            service_resource_type_filters:
                List of :class:`~cloudwanderer.base.ServiceResourceTypeFilter`
                specific to the CloudInterface that helps filter resources.
        """
        for storage_connector in self.storage_connectors:
            storage_connector.open()
        resources = list(
            self.cloud_interface.get_resource(urn=urn, service_resource_type_filters=service_resource_type_filters)
        )

        for resource in resources:
            self._write_resource(resource=resource)
        if not resources:
            for storage_connector in self.storage_connectors:
                storage_connector.delete_resource(urn)

        for storage_connector in self.storage_connectors:
            storage_connector.close()

    def write_resources(
        self,
        regions: Optional[List[str]] = None,
        service_resource_types: Optional[List[ServiceResourceType]] = None,
        service_resource_type_filters: Optional[List[ServiceResourceTypeFilter]] = None,
    ) -> None:
        """Fetch all resources in this account from all regions and all services and write to storage.

        All arguments are optional.

        Example:
            Fetch AWS EC2 VPCs and write to a local Gremlin database.

                >>> from cloudwanderer import CloudWanderer, ServiceResourceType
                >>> from cloudwanderer.storage_connectors import GremlinStorageConnector
                >>> cloud_wanderer = CloudWanderer(storage_connectors=[
                ...        GremlinStorageConnector(
                ...          endpoint_url="ws://localhost:8182",
                ...        )
                ...    ])
                >>> cloud_wanderer.write_resources(
                ...     service_resource_types=[ServiceResourceType("ec2","vpc")]
                ... )

        Arguments:
            regions:
                The name of the region to get resources from (defaults to session default if not specified)
            service_resource_types:
                The resource types to discover.
            service_resource_type_filters:
                List of :class:`~cloudwanderer.base.ServiceResourceTypeFilter`
                specific to the CloudInterface that helps filter resources.

        Raises:
            ValueError: If invalid get/delete urns are produced by the cloud interface's get_resource_discovery_actions
        """
        for storage_connector in self.storage_connectors:
            storage_connector.open()
        action_sets = self.cloud_interface.get_resource_discovery_actions(
            regions=regions, service_resource_types=service_resource_types
        )
        discovery_start_times: Dict[str, datetime] = {}
        for action_set in action_sets:
            for get_urn in action_set.get_urns:
                if not get_urn.region or not get_urn.service or not get_urn.resource_type:
                    raise ValueError(f"Invalid get_urn {get_urn}")

                resources = self.cloud_interface.get_resources(
                    region=get_urn.region,
                    service_name=get_urn.service,
                    resource_type=get_urn.resource_type,
                    service_resource_type_filters=service_resource_type_filters or [],
                )
                for resource in resources:
                    earliest_resource_discovered = discovery_start_times.get(resource.urn.cloud_service_resource_label)
                    if not earliest_resource_discovered or resource.discovery_time < earliest_resource_discovered:
                        discovery_start_times[resource.urn.cloud_service_resource_label] = resource.discovery_time
                    self._write_resource(resource)
            for delete_urn in action_set.delete_urns:
                if (
                    not delete_urn.account_id
                    or not delete_urn.region
                    or not delete_urn.service
                    or not delete_urn.resource_type
                    or not delete_urn.cloud_name
                ):
                    raise ValueError(f"Invalid delete_urn {delete_urn}")
                for storage_connector in self.storage_connectors:
                    storage_connector.delete_resource_of_type_in_account_region(
                        cloud_name=delete_urn.cloud_name,
                        account_id=delete_urn.account_id,
                        region=delete_urn.region,
                        service=delete_urn.service,
                        resource_type=delete_urn.resource_type,
                        cutoff=discovery_start_times.get(delete_urn.cloud_service_resource_label),
                    )
        for storage_connector in self.storage_connectors:
            storage_connector.close()

    def write_resources_concurrently(
        self,
        cloud_interface_generator: Callable,
        storage_connector_generator: Callable,
        concurrency: int = 10,
        **kwargs,
    ) -> List["CloudWandererConcurrentWriteThreadResult"]:
        """Write all resources in this account from all regions and all services to storage.

        Any additional args will be passed into the cloud interface's ``get_`` methods.
        **WARNING:** Experimental.

        Arguments:
            concurrency (int):
                Number of query threads to invoke concurrently.
            cloud_interface_generator (Callable):
                 A method which returns a new cloud interface session when called.
                This helps prevent non-threadsafe cloud interfaces from interfering with each others.
            storage_connector_generator (Callable):
                A method which returns a list of storage connectors when called.
                The returned connectors should be instances of the same connectors each time the method is called.
                These connectors do **not** need to be thread safe and will be returned at the end of execution.
            **kwargs:
                Additional keyword arguments will be passed down to the cloud interface methods.
        """
        logger.info("Writing resources in all regions")
        logger.warning("Using concurrency of: %s - CONCURRENCY IS EXPERIMENTAL", concurrency)
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            threads = []
            for region_name in self.cloud_interface.get_enabled_regions():
                cw = CloudWanderer(
                    storage_connectors=storage_connector_generator(), cloud_interface=cloud_interface_generator()
                )
                threads.append(
                    executor.submit(
                        exception_logging_wrapper,
                        method=cw.write_resources,
                        regions=[region_name],
                        return_value=cw.storage_connectors,
                        **kwargs,
                    )
                )
        thread_results: List[CloudWandererConcurrentWriteThreadResult] = []
        for thread in threads:
            result = thread.result()
            if result:
                thread_results.append(CloudWandererConcurrentWriteThreadResult(storage_connectors=result))
        return thread_results

    def _write_resource(self, resource: CloudWandererResource) -> Union[URN, PartialUrn]:
        for storage_connector in self.storage_connectors:
            storage_connector.write_resource(resource)
        return resource.urn


class CloudWandererConcurrentWriteThreadResult(NamedTuple):
    """The result from write_resources_concurrently."""

    storage_connectors: BaseStorageConnector
