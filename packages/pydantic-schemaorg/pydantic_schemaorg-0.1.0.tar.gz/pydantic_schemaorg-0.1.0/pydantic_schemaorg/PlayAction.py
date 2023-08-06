from pydantic import Field
from pydantic_schemaorg.Audience import Audience
from typing import List, Optional, Union
from pydantic_schemaorg.Event import Event
from pydantic_schemaorg.Action import Action


class PlayAction(Action):
    """The act of playing/exercising/training/performing for enjoyment, leisure, recreation,"
     "Competition or exercise. Related actions: * [[ListenAction]]: Unlike ListenAction"
     "(which is under ConsumeAction), PlayAction refers to performing for an audience or"
     "at an event, rather than consuming music. * [[WatchAction]]: Unlike WatchAction (which"
     "is under ConsumeAction), PlayAction refers to showing/displaying for an audience"
     "or at an event, rather than consuming visual content.

    See https://schema.org/PlayAction.

    """
    type_: str = Field("PlayAction", const=True, alias='@type')
    audience: Optional[Union[List[Union[Audience, str]], Union[Audience, str]]] = Field(
        None,
        description="An intended audience, i.e. a group for whom something was created.",
    )
    event: Optional[Union[List[Union[Event, str]], Union[Event, str]]] = Field(
        None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    

PlayAction.update_forward_refs()
