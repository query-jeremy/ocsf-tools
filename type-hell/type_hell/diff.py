from abc import ABC
from typing import TypeVar, Optional, Generic
from dataclasses import dataclass, field

from type_hell.model import OcsfName, OcsfModel, OcsfAttr, OcsfEvent, OcsfSchema


T = TypeVar("T", covariant=True)


class Difference(Generic[T], ABC): ...


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


#OcsfT = TypeVar("OcsfT", bound=OcsfModel, covariant=True)

class ChangedModel(Difference[T]): ...

class DiffModel(ABC): ...

@dataclass
class DiffAttr(DiffModel, Difference[OcsfAttr]):
    caption: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    max_len: Difference[Optional[int]] = field(default_factory=NoChange[Optional[int]])
    is_array: Difference[bool] = field(default_factory=NoChange[bool])

@dataclass
class DiffEvent(DiffModel, Difference[OcsfEvent]):
    caption: Difference[str] = field(default_factory=NoChange[str])
    name: Difference[str] = field(default_factory=NoChange[str])
    uid: Difference[Optional[int]] = field(default_factory=NoChange[Optional[int]])
    attributes: dict[OcsfName, OcsfAttr] = field(default_factory=dict)

@dataclass
class DiffSchema(DiffModel, Difference[OcsfSchema]):
    version: Difference[str] = field(default_factory=NoChange[str])
    events: dict[OcsfName, OcsfAttr] = field(default_factory=dict)
    base_event: Difference[Optional[OcsfEvent]] = field(default_factory=NoChange[Optional[OcsfEvent]])
