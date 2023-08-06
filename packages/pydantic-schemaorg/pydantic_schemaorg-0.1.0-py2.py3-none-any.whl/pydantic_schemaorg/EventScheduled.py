from pydantic import Field
from pydantic_schemaorg.EventStatusType import EventStatusType


class EventScheduled(EventStatusType):
    """The event is taking place or has taken place on the startDate as scheduled. Use of this"
     "value is optional, as it is assumed by default.

    See https://schema.org/EventScheduled.

    """
    type_: str = Field("EventScheduled", const=True, alias='@type')
    

EventScheduled.update_forward_refs()
