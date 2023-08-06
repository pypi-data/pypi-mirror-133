from pydantic import Field
from decimal import Decimal
from typing import List, Optional, Union
from pydantic_schemaorg.Comment import Comment
from pydantic_schemaorg.RsvpResponseType import RsvpResponseType
from pydantic_schemaorg.InformAction import InformAction


class RsvpAction(InformAction):
    """The act of notifying an event organizer as to whether you expect to attend the event.

    See https://schema.org/RsvpAction.

    """
    type_: str = Field("RsvpAction", const=True, alias='@type')
    additionalNumberOfGuests: Optional[Union[List[Union[Decimal, str]], Union[Decimal, str]]] = Field(
        None,
        description="If responding yes, the number of guests who will attend in addition to the invitee.",
    )
    comment: Optional[Union[List[Union[Comment, str]], Union[Comment, str]]] = Field(
        None,
        description="Comments, typically from users.",
    )
    rsvpResponse: Optional[Union[List[Union[RsvpResponseType, str]], Union[RsvpResponseType, str]]] = Field(
        None,
        description="The response (yes, no, maybe) to the RSVP.",
    )
    

RsvpAction.update_forward_refs()
