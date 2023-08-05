"""Models for CloudWanderer data."""
from enum import Enum, IntEnum, auto, unique
from typing import Any, Dict, List, NamedTuple

from .urn import PartialUrn


class ActionSet(NamedTuple):
    """Define a list of partial URNs to discover and delete."""

    #: The URNs to get
    get_urns: List[PartialUrn]
    #: The URNs to delete
    delete_urns: List[PartialUrn]


class TemplateActionSet(ActionSet):
    """An set of actions which have not yet had all their placeholders inflated.

    This differs from a regular ActionSet action insofar as it
    will probably contain actions with the region :attr:`TemplateActionSetRegionValues.ALL_REGIONS`.
    These actions need to be unpacked into region specific actions that
    reflect the enabled regions in the AWS account in question
    before being placed into a non-cloud specific ActionSet class
    for CloudWanderer to consume.
    """

    def inflate(self, regions: List[str], account_id: str) -> ActionSet:
        new_action_set = ActionSet(get_urns=[], delete_urns=[])
        for partial_urn in self.get_urns:
            new_action_set.get_urns.extend(self._inflate_partial_urn(partial_urn, account_id, regions))

        for partial_urn in self.delete_urns:
            new_action_set.delete_urns.extend(self._inflate_partial_urn(partial_urn, account_id, regions))

        return new_action_set

    @staticmethod
    def _inflate_partial_urn(partial_urn: PartialUrn, account_id: str, regions: List[str]) -> List[PartialUrn]:
        if partial_urn.region != TemplateActionSetRegionValues.ALL_REGIONS.name:
            return [partial_urn.copy(account_id=account_id)]

        inflated_partial_urns = []
        for region in regions:
            inflated_partial_urns.append(partial_urn.copy(account_id=account_id, region=region))
        return inflated_partial_urns


@unique
class TemplateActionSetRegionValues(IntEnum):
    """The possible template values for regions."""

    #: The action template applies to all regions
    ALL_REGIONS = auto()


class ServiceResourceType(NamedTuple):
    """A resource type including a service that it is member of.

    Example:
        Creating an S3 bucket resource type:

        >>> from cloudwanderer import ServiceResourceType
        >>> print(ServiceResourceType(service="s3", resource_type="bucket"))
        ServiceResourceType(service='s3', resource_type='bucket')
    """

    #: The name of the service
    service: str
    #: The type of resource (snake_case)
    resource_type: str


class Relationship(NamedTuple):
    """Specifying the relationship between two resources."""

    partial_urn: PartialUrn
    direction: "RelationshipDirection"


@unique
class RelationshipAccountIdSource(Enum):
    """Enum specifying the source of a relationship's Account ID."""

    UNKNOWN = auto()
    SAME_AS_RESOURCE = auto()


@unique
class RelationshipRegionSource(Enum):
    """Enum specifying the source of a relationship's Region."""

    UNKNOWN = auto()
    SAME_AS_RESOURCE = auto()


@unique
class RelationshipDirection(Enum):
    """Enum specifying the direction of a relationship."""

    OUTBOUND = auto()
    INBOUND = auto()


@unique
class ResourceIndependenceType(Enum):
    """Enum specifying whether this resource requires a parent resource for id uniqueness."""

    BASE_RESOURCE = auto()
    DEPENDENT_RESOURCE = auto()
    SECONDARY_ATTRIBUTE = auto()


class ResourceIdUniquenessScope(NamedTuple):
    """What is the scope of this resource ID's uniqueness.

    This is not used at runtime but is used by tests to determine the validity of relationship specifications.
    """

    #: The resource id is only unique if the region is also supplied
    requires_region: bool
    #: The resource id is only unique if the account id is also supplied
    requires_account_id: bool

    @classmethod
    def factory(cls, raw_dict: Dict[str, Any]) -> "ResourceIdUniquenessScope":
        return cls(
            requires_region=raw_dict.get("requiresRegion", True),
            requires_account_id=raw_dict.get("requiresAccountId", True),
        )
