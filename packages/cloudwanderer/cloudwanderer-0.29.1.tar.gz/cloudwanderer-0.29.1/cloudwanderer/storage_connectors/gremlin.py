"""Storage Connector for Gremlin databases."""
import logging
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional, Union, cast

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection  # type: ignore
from gremlin_python.process.anonymous_traversal import traversal  # type: ignore
from gremlin_python.process.graph_traversal import __  # type: ignore
from gremlin_python.process.traversal import Cardinality, P, T, Traversal  # type: ignore

from cloudwanderer.models import RelationshipDirection

from ..cloud_wanderer_resource import CloudWandererResource
from ..urn import URN, PartialUrn
from .base_connector import ISO_DATE_FORMAT, BaseStorageConnector

logger = logging.getLogger(__name__)


def generate_primary_label(urn: PartialUrn) -> str:
    """Generate a primary vertex label.

    Arguments:
        urn: The URN to generate the vertex label from.
    """
    return urn.cloud_service_resource_label


class GremlinStorageConnector(BaseStorageConnector):
    """Storage Connector for Gremlin databases."""

    _g: Optional[Traversal] = None
    connection: Optional[DriverRemoteConnection] = None

    def __init__(self, endpoint_url: str, supports_multiple_labels=False, test_prefix: str = "", **kwargs) -> None:
        """Create a GremlinStorageConnector.

        Arguments:
            endpoint_url: The url of the gremlin endpoint to connect to (e.g. ``ws://localhost:8182``)
            supports_multiple_labels: Some GraphDBs (Neptune/Neo4J) support multiple labels on a single vertex.
            test_prefix: A prefix that will be prepended to edge and vertex ids to allow scenario separation.
            **kwargs: Any unspecified args will be pased to the ``DriverRemoteConnection`` object.
        """
        self.endpoint_url = endpoint_url
        self.supports_multiple_labels = supports_multiple_labels
        self.test_prefix = test_prefix
        self.connection_args = kwargs

    def init(self) -> None:
        ...

    @property
    def g(self) -> Traversal:
        if not self.connection:
            self.open()
        if not self._g:
            self._g = traversal().withRemote(self.connection)
        return self._g

    def open(self) -> DriverRemoteConnection:
        if not self.connection:
            logger.debug("Opening connection to %s", self.endpoint_url)
            self.connection = DriverRemoteConnection(f"{self.endpoint_url}/gremlin", "g", **self.connection_args)

    def close(self) -> None:
        logger.debug("Closing gremlin connection")
        if self.connection:
            self.connection.close()
        self.connection = None
        self._g = None

    def write_resource(self, resource: CloudWandererResource) -> None:
        """Persist a single resource to storage.

        Arguments:
            resource (CloudWandererResource): The CloudWandererResource to write.
        """
        self._write_resource(resource)
        self._write_dependent_resource_edges(resource)

    def _write_resource(self, resource: CloudWandererResource) -> None:
        primary_label = generate_primary_label(resource.urn)

        traversal = self._write_vertex(vertex_id=self.generate_vertex_id(resource.urn), vertex_labels=[primary_label])
        traversal = (
            traversal.property(Cardinality.single, "_cloud_name", resource.urn.cloud_name)
            .property(Cardinality.single, "_account_id", resource.urn.account_id)
            .property(Cardinality.single, "_region", resource.urn.region)
            .property(Cardinality.single, "_service", resource.urn.service)
            .property(Cardinality.single, "_resource_type", resource.urn.resource_type)
            .property(Cardinality.single, "_discovery_time", resource.discovery_time.isoformat())
            .property(Cardinality.single, "_urn", str(resource.urn))
        )
        for id_part in resource.urn.resource_id_parts:
            traversal.property(Cardinality.set_, "_resource_id_parts", id_part)
        self._write_properties(traversal=traversal, properties=resource.cloudwanderer_metadata.resource_data)

        self._write_relationships(resource)
        self._clean_up_relationships(urn=resource.urn, cutoff=resource.discovery_time)
        if not resource.urn.is_partial:
            self._repoint_vertex_edges(vertex_label=primary_label, new_resource_urn=resource.urn)

    def _write_dependent_resource_edges(self, resource: CloudWandererResource) -> None:
        for dependent_urn in resource.dependent_resource_urns:
            logger.debug("Writing dependent resource edge from %s to %s", resource.urn, dependent_urn)
            self._write_edge(
                edge_id=self.generate_edge_id(resource.urn, dependent_urn),
                edge_label="has",
                source_vertex_id=self.generate_vertex_id(resource.urn),
                destination_vertex_id=self.generate_vertex_id(dependent_urn),
                owner_id=self.generate_vertex_id(resource.urn),
                discovery_time=resource.discovery_time,
            )

    def _clean_up_relationships(self, urn: PartialUrn, cutoff: datetime) -> None:
        logger.debug("Cleaning up edges owned by %s discovered before %s", self.generate_vertex_id(urn), cutoff)
        (
            self.g.V(self.generate_vertex_id(urn))
            .bothE()
            .as_("edge")
            .has("_edge_owner", self.generate_vertex_id(urn))
            .where(__.values("_discovery_time").is_(P.lt(cutoff.isoformat())))
            .select("edge")
            .drop()
        ).iterate()

    def _write_relationships(self, resource: CloudWandererResource) -> None:
        for relationship in resource.relationships:
            inferred_partner_urn = relationship.partial_urn
            try:
                pre_existing_resource_urn = (
                    self._lookup_resource(relationship.partial_urn).propertyMap().toList()[0]["_urn"][0].value
                )
            except IndexError:
                pre_existing_resource_urn = None

            if pre_existing_resource_urn:
                logger.debug("Writing relationship with pre_existing_resource_urn %s", pre_existing_resource_urn)
                self._write_relationship_edge(
                    resource_urn=resource.urn,
                    relationship_resource_urn=pre_existing_resource_urn,
                    direction=relationship.direction,
                    discovery_time=resource.discovery_time,
                )
                if pre_existing_resource_urn != inferred_partner_urn:
                    self._delete_relationship_edge(
                        resource_urn=resource.urn,
                        relationship_resource_urn=inferred_partner_urn,
                        direction=relationship.direction,
                    )
                continue
            logger.debug("Writing inferred resource %s", inferred_partner_urn)
            self._write_resource(CloudWandererResource(urn=cast(URN, relationship.partial_urn), resource_data={}))
            self._write_relationship_edge(
                resource_urn=resource.urn,
                relationship_resource_urn=inferred_partner_urn,
                direction=relationship.direction,
                discovery_time=resource.discovery_time,
            )

    def _repoint_vertex_edges(self, vertex_label: str, new_resource_urn: Union[URN, PartialUrn]) -> None:
        # https://tinkerpop.apache.org/docs/current/recipes/#edge-move

        resources_of_the_same_type = self.g.V().as_("old_vertex").hasLabel(vertex_label)
        for id_part in new_resource_urn.resource_id_parts:
            resources_of_the_same_type.has("_resource_id_parts", id_part)
        resources_with_same_id_but_unknown = (
            resources_of_the_same_type.or_(__.has("_account_id", "unknown"), __.has("_region", "unknown"))
        ).toList()

        for old_vertex in resources_with_same_id_but_unknown:
            # Outbound
            old_vertices_outbound_edges = self.g.V(old_vertex).outE().as_("e1")
            old_outbound_edges_partner_vertex = old_vertices_outbound_edges.inV().as_("b")

            new_vertex = old_outbound_edges_partner_vertex.V(self.generate_vertex_id(new_resource_urn)).as_(
                "new_vertex"
            )
            add_old_outbound_edges_to_new_vertex = (
                new_vertex.addE("has")
                .to("b")
                .as_("e2")
                .sideEffect(
                    __.select("e1")
                    .properties()
                    .unfold()
                    .as_("p")
                    .select("e2")
                    .property(__.select("p").key(), __.select("p").value())
                )
            )
            add_old_outbound_edges_to_new_vertex.select("e1").drop().iterate()
            # Inbound
            old_vertices_inbound_edges = self.g.V(old_vertex).select("old_vertex").inE().as_("old_inbound_edge")
            old_inbound_edges_partner_vertex = old_vertices_inbound_edges.inV().as_("c")

            new_vertex = old_inbound_edges_partner_vertex.select("new_vertex")
            add_old_inbound_edges_to_new_vertex = (
                new_vertex.addE("has")
                .from_("c")
                .as_("new_inbound_edge")
                .sideEffect(
                    __.select("old_inbound_edge")
                    .properties()
                    .unfold()
                    .as_("p")
                    .select("new_inbound_edge")
                    .property(__.select("p").key(), __.select("p").value())
                )
            )
            add_old_inbound_edges_to_new_vertex.select("old_inbound_edge").drop().iterate()

            # Delete old vertex
            self.g.V(old_vertex).drop().iterate()

    def _delete_relationship_edge(
        self, resource_urn: PartialUrn, relationship_resource_urn: PartialUrn, direction: RelationshipDirection
    ) -> None:
        if direction == RelationshipDirection.INBOUND:
            self._delete_edge(self.generate_edge_id(relationship_resource_urn, resource_urn))
        else:
            self._delete_edge(self.generate_edge_id(resource_urn, relationship_resource_urn))

    def _write_relationship_edge(
        self,
        resource_urn: PartialUrn,
        relationship_resource_urn: PartialUrn,
        direction: RelationshipDirection,
        discovery_time: datetime,
    ) -> None:
        logger.debug("Writing edge relationship between %s and %s", resource_urn, relationship_resource_urn)
        if direction == RelationshipDirection.INBOUND:
            self._write_edge(
                edge_id=self.generate_edge_id(relationship_resource_urn, resource_urn),
                edge_label="has",
                source_vertex_id=self.generate_vertex_id(relationship_resource_urn),
                destination_vertex_id=self.generate_vertex_id(resource_urn),
                owner_id=self.generate_vertex_id(resource_urn),
                discovery_time=discovery_time,
            )
        else:
            self._write_edge(
                edge_id=self.generate_edge_id(resource_urn, relationship_resource_urn),
                edge_label="has",
                source_vertex_id=self.generate_vertex_id(resource_urn),
                destination_vertex_id=self.generate_vertex_id(relationship_resource_urn),
                owner_id=self.generate_vertex_id(resource_urn),
                discovery_time=discovery_time,
            )

    def _lookup_resource(self, partial_urn: PartialUrn) -> Traversal:
        vertex_label = generate_primary_label(partial_urn)
        logger.debug("looking up resource with label %s", vertex_label)
        traversal = (
            self.g.V()
            .hasLabel(vertex_label)
            .has("_cloud_name", partial_urn.cloud_name)
            .has("_service", partial_urn.service)
            .has("_resource_type", partial_urn.resource_type)
        )
        for id_part in partial_urn.resource_id_parts:
            traversal.has("_resource_id_parts", id_part)
        if partial_urn.account_id != "unknown":
            traversal.has("_account_id", partial_urn.account_id)
        if partial_urn.region != "unknown":
            traversal.has("_region", partial_urn.region)
        return traversal

    def _write_vertex(self, vertex_id: str, vertex_labels: List[str]) -> Traversal:
        logger.debug("Writing vertex %s", vertex_id)
        if self.supports_multiple_labels:
            vertex_label = "::".join(vertex_labels)
        else:
            vertex_label = vertex_labels[0]
        return self.g.V(vertex_id).fold().coalesce(__.unfold(), __.addV(vertex_label).property(T.id, vertex_id))

    def _write_properties(self, traversal: Traversal, properties: Dict[str, Any]) -> Traversal:
        logger.debug("Writing properties: %s", properties)
        for property_name, property_value in properties.items():
            traversal = traversal.property(Cardinality.single, str(property_name), str(property_value))
        traversal_size = len(str(traversal).encode())
        try:
            traversal.next()
        except RuntimeError as ex:
            raise RuntimeError(
                "GremlinStorageConnector got a runtime error while saving a property of "
                f"{traversal_size} bytes, check your Gremlin server's maxContentLength is larger than this."
            ) from ex

    def _write_edge(
        self,
        edge_id: str,
        edge_label: str,
        source_vertex_id: str,
        destination_vertex_id: str,
        owner_id: str,
        discovery_time: datetime,
    ) -> Traversal:
        logger.debug("Looking for edge %s", edge_id)
        edge = self.g.E(edge_id).property("_discovery_time", discovery_time.isoformat()).toList()

        if not edge:
            logger.debug("Writing edge between %s and %s", source_vertex_id, destination_vertex_id)
            (
                self.g.V(source_vertex_id)
                .as_("source")
                .V(destination_vertex_id)
                .addE(edge_label)
                .from_("source")
                .property(T.id, edge_id)
                .property("_edge_owner", owner_id)
                .property("_discovery_time", discovery_time.isoformat())
            ).next()

    def _delete_edge(self, edge_id: str) -> Traversal:
        logger.debug("Deleting edge %s", edge_id)
        self.g.E(edge_id).drop().iterate()

    def read_all(self) -> Iterator[dict]:
        """Return all records from storage."""
        for vertex in self.g.V().has("_urn").valueMap().toList():
            yield vertex

    def read_resource(self, urn: URN) -> Optional[CloudWandererResource]:
        """Return a resource matching the supplied urn from storage.

        Arguments:
            urn (URN): The AWS URN of the resource to return
        """
        return next(self.read_resources(urn=urn))

    def read_resources(
        self,
        cloud_name: str = None,
        account_id: str = None,
        region: str = None,
        service: str = None,
        resource_type: str = None,
        urn: Union[URN, PartialUrn] = None,
    ) -> Iterator["CloudWandererResource"]:
        """Yield a resource matching the supplied urn from storage.

        All arguments are optional.

        Arguments:
            cloud_name: The name of the cloud in question (e.g. ``aws``)
            urn: The AWS URN of the resource to return
            account_id: Cloud Account ID (e.g. ``111111111111``)
            region: AWS region (e.g. ``'eu-west-2'``)
            service: Service name (e.g. ``'ec2'``)
            resource_type: Resource Type (e.g. ``'instance'``)
        """
        if not urn:
            urn = PartialUrn(
                cloud_name=cloud_name or "unknown",
                service=service or "unknown",
                account_id=account_id or "unknown",
                region=region or "unknown",
                resource_type=resource_type or "unknown",
            )
        for vertex in self._lookup_resource(partial_urn=urn).propertyMap().toList():
            yield CloudWandererResource(
                urn=URN.from_string(vertex["_urn"][0].value),
                resource_data=_normalise_gremlin_attrs(vertex),
                discovery_time=datetime.strptime(vertex["_discovery_time"][0].value, ISO_DATE_FORMAT),
            )

    def delete_resource(self, urn: URN) -> None:
        """Delete this resource and all its resource attributes.

        Arguments:
            urn (URN): The URN of the resource to delete
        """
        logger.debug("Deleting resource %s", urn)
        self.g.V(self.generate_vertex_id(urn)).drop().iterate()

    def delete_resource_of_type_in_account_region(
        self,
        cloud_name: str,
        service: str,
        resource_type: str,
        account_id: str,
        region: str,
        cutoff: Optional[datetime],
    ) -> None:
        """Delete resources of type in account and region unless in list of URNs.

        This is used primarily to clean up old resources.

        Arguments:
            cloud_name: The name of the cloud in question (e.g. ``aws``)
            account_id: Cloud Account ID (e.g. ``111111111111``)
            region: Cloud region (e.g. ``'eu-west-2'``)
            service: Service name (e.g. ``'ec2'``)
            resource_type: Resource Type (e.g. ``'instance'``)
            cutoff: Delete any resource discovered before this time
        """
        partial_urn = PartialUrn(
            cloud_name=cloud_name,
            service=service,
            account_id=account_id,
            region=region,
            resource_type=resource_type,
        )
        logger.debug("Deleting resources that match %s that were discovered before %s", partial_urn, cutoff)
        traversal = self._lookup_resource(partial_urn=partial_urn)
        if cutoff:
            traversal.where(__.values("_discovery_time").is_(P.lt(cutoff.isoformat())))
        traversal.drop().iterate()

    def generate_vertex_id(self, urn: PartialUrn) -> str:
        """Generate a vertex id.

        Arguments:
            urn: The URN of the vertex to create.
        """
        return f"{self.test_prefix}{urn}"

    def generate_edge_id(self, source_urn: PartialUrn, destination_urn: PartialUrn) -> str:
        """Generate a primary edge id.

        Arguments:
            source_urn: The URN of the resource we're generating an edge from.
            destination_urn: The URN of the resource we're generating an edge to.
        """
        logger.debug("Generating edge id: %s", source_urn)
        return f"{self.test_prefix}{source_urn}#{destination_urn}"


def _normalise_gremlin_attrs(raw_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Remove any underscore prefixed keys as these are attributes we use to identify the DynamoDB record.

    Arguments:
        raw_dict: The raw dictionary of the DynamoDB record that needs cleaning.
    """
    # TODO: add list support in gremlin
    normalised_dict = {k: v[0].value for k, v in raw_dict.items() if not k.startswith("_")}
    return normalised_dict
