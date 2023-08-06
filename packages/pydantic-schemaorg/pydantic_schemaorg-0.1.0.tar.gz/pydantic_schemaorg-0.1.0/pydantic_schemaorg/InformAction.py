from pydantic import Field
from pydantic_schemaorg.Event import Event
from typing import List, Optional, Union
from pydantic_schemaorg.CommunicateAction import CommunicateAction


class InformAction(CommunicateAction):
    """The act of notifying someone of information pertinent to them, with no expectation of"
     "a response.

    See https://schema.org/InformAction.

    """
    type_: str = Field("InformAction", const=True, alias='@type')
    event: Optional[Union[List[Union[Event, str]], Union[Event, str]]] = Field(
        None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    

InformAction.update_forward_refs()
