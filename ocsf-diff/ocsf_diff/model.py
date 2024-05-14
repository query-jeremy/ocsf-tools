"""Model for comparing OCSF schemata

Notes:
 - Everything inherits from Difference[T]
 - None has been replaced with NoChange[T]
 - Dicts of [str, OcsfModel] always have all keys from both operands.
 - Be warned that OcsfAttr.enum is Optional[dict[str, OcsfEnumMember]] and so it may be NoChange[OcsfEnumMember] instead of an empty dict.
 - Dicts of primitives:
    - OcsfInclude.annotations
    - OcsfProfile.annotations
    - OcsfObject.constraints
    - OcsfEvent.constraints
"""

from dataclasses import dataclass, field
from typing import Any, TypeVar, Generic, Optional
from abc import ABC

from ocsf_schema import (
    OcsfVersion,
    OcsfT,
    OcsfModel,
    OcsfEnumMember,
    OcsfAttr,
    OcsfDeprecationInfo,
    OcsfType,
    OcsfObject,
    OcsfEvent,
    OcsfSchema,
)


T = TypeVar("T", covariant=True)


class Difference(ABC, Generic[T]): ...


@dataclass
class Addition(Difference[T]):
    after: T


@dataclass
class Removal(Difference[T]):
    before: T


@dataclass
class Change(Difference[T]):
    before: Optional[T]
    after: Optional[T]


@dataclass
class NoChange(Difference[T]): ...


class ChangedModel(Difference[OcsfT]): ...


class DiffModel(ChangedModel[OcsfModel]): ...


@dataclass
class DiffVersion(ChangedModel[OcsfVersion]):
    version: Difference[str] = field(default_factory=NoChange)


@dataclass
class DiffEnumMember(ChangedModel[OcsfEnumMember]):
    caption: Difference[str] = field(default_factory=NoChange)
    description: Difference[Optional[str]] = field(default_factory=NoChange)
    notes: Difference[Optional[str]] = field(default_factory=NoChange)


@dataclass
class DiffDeprecationInfo(ChangedModel[OcsfDeprecationInfo]):
    message: Difference[str] = field(default_factory=NoChange)
    since: Difference[str] = field(default_factory=NoChange)


@dataclass
class DiffType(ChangedModel[OcsfType]):
    caption: Difference[str] = field(default_factory=NoChange)
    description: Difference[str] = field(default_factory=NoChange)
    is_array: Difference[bool] = field(default_factory=NoChange)
    deprecated: Difference[Optional[DiffDeprecationInfo]] = field(default_factory=NoChange)
    max_len: Difference[Optional[int]] = field(default_factory=NoChange)
    observable: Difference[Optional[int]] = field(default_factory=NoChange)
    range: Difference[Optional[list[int]]] = field(default_factory=NoChange)
    regex: Difference[Optional[str]] = field(default_factory=NoChange)
    type: Difference[Optional[str]] = field(default_factory=NoChange)
    type_name: Difference[Optional[str]] = field(default_factory=NoChange)
    values: Difference[Optional[list[Any]]] = field(default_factory=NoChange)


@dataclass
class DiffAttr(ChangedModel[OcsfAttr]):
    caption: Difference[str] = field(default_factory=NoChange)
    description: Difference[str] = field(default_factory=NoChange)
    requirement: Difference[str] = field(default_factory=NoChange)
    type: Difference[str] = field(default_factory=NoChange)
    is_array: Difference[bool] = field(default_factory=NoChange)
    enum: dict[str, Difference[OcsfEnumMember]] | NoChange[None] = field(default_factory=NoChange)
    group: Difference[Optional[str]] = field(default_factory=NoChange)
    observable: Difference[Optional[int]] = field(default_factory=NoChange)
    sibling: Difference[Optional[str]] = field(default_factory=NoChange)
    profile: Difference[Optional[str | list[str]]] = field(default_factory=NoChange)
    deprecated: Difference[Optional[OcsfDeprecationInfo]] = field(default_factory=NoChange)


@dataclass
class DiffObject(ChangedModel[OcsfObject]):
    caption: Difference[str] = field(default_factory=NoChange)
    name: Difference[str] = field(default_factory=NoChange)
    attributes: dict[str, Difference[OcsfAttr]] = field(default_factory=dict)
    description: Difference[str] = field(default_factory=NoChange)
    extends: Difference[Optional[str]] = field(default_factory=NoChange)
    observable: Difference[Optional[int]] = field(default_factory=NoChange)
    profiles: Difference[Optional[list[str]]] = field(default_factory=NoChange)
    constraints: Difference[Optional[dict[str, list[str]]]] = field(default_factory=NoChange)
    deprecated: Difference[Optional[OcsfDeprecationInfo]] = field(default_factory=NoChange)


@dataclass
class DiffEvent(ChangedModel[OcsfEvent]):
    caption: Difference[str] = field(default_factory=NoChange)
    name: Difference[str] = field(default_factory=NoChange)
    attributes: dict[str, Difference[OcsfAttr]] = field(default_factory=dict)
    description: Difference[Optional[str]] = field(default_factory=NoChange)

    uid: Difference[Optional[int]] = field(default_factory=NoChange)
    category: Difference[Optional[str]] = field(default_factory=NoChange)
    extends: Difference[Optional[str]] = field(default_factory=NoChange)
    profiles: Difference[Optional[list[str]]] = field(default_factory=NoChange)
    associations: Difference[Optional[dict[str, list[str]]]] = field(default_factory=NoChange)
    constraints: Difference[Optional[dict[str, list[str]]]] = field(default_factory=NoChange)
    include: Difference[Optional[str]] = field(default_factory=NoChange)
    deprecated: Difference[Optional[OcsfDeprecationInfo]] = field(default_factory=NoChange)


@dataclass
class DiffSchema(ChangedModel[OcsfSchema]):
    classes: dict[str, Difference[OcsfEvent]] = field(default_factory=dict)
    objects: dict[str, Difference[OcsfObject]] = field(default_factory=dict)
    version: Difference[OcsfVersion] = field(default_factory=NoChange)
    types: dict[str, DiffType] = field(default_factory=dict)
    base_event: Difference[Optional[OcsfEvent]] = field(default_factory=NoChange)
