from pydantic import Field
from pydantic_schemaorg.EntertainmentBusiness import EntertainmentBusiness
from typing import List, Optional, Union
from pydantic_schemaorg.PlayAction import PlayAction


class PerformAction(PlayAction):
    """The act of participating in performance arts.

    See https://schema.org/PerformAction.

    """
    type_: str = Field("PerformAction", const=True, alias='@type')
    entertainmentBusiness: Optional[Union[List[Union[EntertainmentBusiness, str]], Union[EntertainmentBusiness, str]]] = Field(
        None,
        description="A sub property of location. The entertainment business where the action occurred.",
    )
    

PerformAction.update_forward_refs()
